from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils import timezone
from django.utils.html import format_html
from django.db.models import Count, Sum
from django.urls import reverse
from .models import (
    User, Tournament, TournamentParticipant, TournamentResult, Transaction,
    PaymentRequest, PaymentMethod, PaymentQR, Game, StoreItem, Order, Notification,
    FullTournament, FullTournamentParticipant
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom user admin"""
    list_display = ['username', 'user_id', 'email', 'coins', 'total_tournaments_won', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    search_fields = ['username', 'email', 'user_id']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Gaming Profile', {
            'fields': ('user_id', 'phone', 'coins', 'referral_code', 'referred_by', 
                      'avatar', 'total_tournaments_won', 'total_tournaments_played')
        }),
    )
    
    readonly_fields = ['user_id', 'referral_code']
    
    actions = ['add_coins', 'deduct_coins']
    
    def add_coins(self, request, queryset):
        """Add coins to selected users"""
        for user in queryset:
            user.coins += 100
            user.save()
            Transaction.objects.create(
                user=user,
                transaction_type='admin_adjustment',
                amount=100,
                description='Admin bonus',
                balance_after=user.coins
            )
        self.message_user(request, f'Added 100 coins to {queryset.count()} users')
    add_coins.short_description = 'Add 100 coins to selected users'
    
    def deduct_coins(self, request, queryset):
        """Deduct coins from selected users"""
        for user in queryset:
            if user.coins >= 50:
                user.coins -= 50
                user.save()
                Transaction.objects.create(
                    user=user,
                    transaction_type='admin_adjustment',
                    amount=-50,
                    description='Admin deduction',
                    balance_after=user.coins
                )
        self.message_user(request, f'Deducted 50 coins from eligible users')
    deduct_coins.short_description = 'Deduct 50 coins from selected users'


class TournamentParticipantInline(admin.TabularInline):
    """Inline for tournament participants"""
    model = TournamentParticipant
    extra = 0
    readonly_fields = ['user', 'joined_at']
    fields = ['user', 'in_game_name', 'in_game_id', 'position', 'prize_won', 'joined_at']


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    """Tournament admin"""
    list_display = ['title', 'game', 'entry_fee', 'prize_pool', 'tournament_date', 'status', 'current_participants', 'max_participants']
    list_filter = ['game', 'status', 'tournament_date']
    search_fields = ['title', 'description']
    date_hierarchy = 'tournament_date'
    inlines = [TournamentParticipantInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'game', 'description', 'image')
        }),
        ('Tournament Details', {
            'fields': ('entry_fee', 'prize_pool', 'max_participants', 'tournament_date', 'status')
        }),
        ('Room Information', {
            'fields': ('room_id', 'room_password')
        }),
    )
    
    actions = ['start_tournament', 'complete_tournament', 'cancel_tournament']
    
    def start_tournament(self, request, queryset):
        """Start selected tournaments"""
        queryset.update(status='ongoing')
        self.message_user(request, f'Started {queryset.count()} tournaments')
    start_tournament.short_description = 'Start selected tournaments'
    
    def complete_tournament(self, request, queryset):
        """Complete selected tournaments"""
        queryset.update(status='completed')
        self.message_user(request, f'Completed {queryset.count()} tournaments')
    complete_tournament.short_description = 'Complete selected tournaments'
    
    def cancel_tournament(self, request, queryset):
        """Cancel selected tournaments and refund entry fees"""
        for tournament in queryset:
            participants = TournamentParticipant.objects.filter(tournament=tournament)
            for participant in participants:
                user = participant.user
                user.coins += tournament.entry_fee
                user.save()
                
                Transaction.objects.create(
                    user=user,
                    transaction_type='admin_adjustment',
                    amount=tournament.entry_fee,
                    description=f'Refund for cancelled tournament: {tournament.title}',
                    balance_after=user.coins
                )
                
                Notification.objects.create(
                    user=user,
                    notification_type='tournament',
                    title='Tournament Cancelled',
                    message=f'{tournament.title} has been cancelled. Your entry fee has been refunded.'
                )
        
        queryset.update(status='cancelled')
        self.message_user(request, f'Cancelled {queryset.count()} tournaments and refunded participants')
    cancel_tournament.short_description = 'Cancel selected tournaments (with refund)'


@admin.register(TournamentParticipant)
class TournamentParticipantAdmin(admin.ModelAdmin):
    """Tournament participant admin"""
    list_display = ['user', 'tournament', 'in_game_name', 'position', 'prize_won', 'joined_at']
    list_filter = ['tournament__game', 'joined_at']
    search_fields = ['user__username', 'tournament__title', 'in_game_name', 'in_game_id']
    date_hierarchy = 'joined_at'
    
    fieldsets = (
        ('Participant Info', {
            'fields': ('tournament', 'user', 'in_game_name', 'in_game_id')
        }),
        ('Results', {
            'fields': ('position', 'prize_won')
        }),
    )
    
    actions = ['award_prize']


@admin.register(TournamentResult)
class TournamentResultAdmin(admin.ModelAdmin):
    """Tournament result admin - Resolve disputes"""
    list_display = ['tournament_link', 'user', 'result_claim', 'screenshot_preview', 'status_badge', 'submitted_at']
    list_filter = ['status', 'result_claim', 'submitted_at']
    search_fields = ['user__username', 'tournament__title']
    date_hierarchy = 'submitted_at'
    list_per_page = 20
    
    fieldsets = (
        ('Result Details', {
            'fields': ('tournament', 'user', 'result_claim', 'status')
        }),
        ('Proof', {
            'fields': ('screenshot', 'screenshot_display')
        }),
        ('Admin Actions', {
            'fields': ('admin_notes',)
        }),
    )
    
    readonly_fields = ['tournament', 'user', 'result_claim', 'submitted_at', 'screenshot_display']
    
    actions = ['declare_player1_winner', 'declare_player2_winner']
    
    def tournament_link(self, obj):
        """Display tournament with link"""
        return format_html(
            '<a href="/admin/core/tournament/{}/change/">{}</a>',
            obj.tournament.id,
            obj.tournament.title
        )
    tournament_link.short_description = 'Tournament'
    
    def status_badge(self, obj):
        """Display status with color badge"""
        colors = {
            'pending': '#FFA500',
            'verified': '#10b981',
            'disputed': '#ef4444',
            'resolved': '#3b82f6'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 12px; font-weight: bold;">{}</span>',
            colors.get(obj.status, '#6B7280'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def screenshot_preview(self, obj):
        """Display screenshot preview"""
        if obj.screenshot:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 8px; border: 2px solid #e5e7eb;" /></a>',
                obj.screenshot.url,
                obj.screenshot.url
            )
        return '-'
    screenshot_preview.short_description = 'Screenshot'
    
    def screenshot_display(self, obj):
        """Display full screenshot in detail view"""
        if obj.screenshot:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="max-width: 600px; max-height: 600px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);" /></a><br><br><a href="{}" target="_blank" class="button">View Full Size</a>',
                obj.screenshot.url,
                obj.screenshot.url,
                obj.screenshot.url
            )
        return 'No screenshot uploaded'
    screenshot_display.short_description = 'Result Screenshot'
    
    def declare_player1_winner(self, request, queryset):
        """Declare first player as winner in disputed results"""
        from .views import award_winner
        
        tournaments = set()
        for result in queryset.filter(status='disputed'):
            tournaments.add(result.tournament)
        
        for tournament in tournaments:
            results = TournamentResult.objects.filter(tournament=tournament, status='disputed')
            if results.count() == 2:
                player1 = results[0].user
                player2 = results[1].user
                
                award_winner(tournament, player1, player2)
                
                results.update(status='resolved', admin_notes=f'Admin declared {player1.username} as winner')
        
        self.message_user(request, f'Resolved {len(tournaments)} disputed tournaments')
    declare_player1_winner.short_description = 'Declare Player 1 as Winner'
    
    def declare_player2_winner(self, request, queryset):
        """Declare second player as winner in disputed results"""
        from .views import award_winner
        
        tournaments = set()
        for result in queryset.filter(status='disputed'):
            tournaments.add(result.tournament)
        
        for tournament in tournaments:
            results = TournamentResult.objects.filter(tournament=tournament, status='disputed')
            if results.count() == 2:
                player1 = results[0].user
                player2 = results[1].user
                
                award_winner(tournament, player2, player1)
                
                results.update(status='resolved', admin_notes=f'Admin declared {player2.username} as winner')
        
        self.message_user(request, f'Resolved {len(tournaments)} disputed tournaments')
    declare_player2_winner.short_description = 'Declare Player 2 as Winner'
    
    def award_prize(self, request, queryset):
        """Award prizes to selected participants"""
        for participant in queryset:
            if participant.prize_won > 0:
                user = participant.user
                user.coins += participant.prize_won
                
                if participant.position == 1:
                    user.total_tournaments_won += 1
                
                user.save()
                
                Transaction.objects.create(
                    user=user,
                    transaction_type='tournament_win',
                    amount=participant.prize_won,
                    description=f'Prize for {participant.tournament.title} (Position: {participant.position})',
                    balance_after=user.coins
                )
                
                Notification.objects.create(
                    user=user,
                    notification_type='tournament',
                    title='Prize Won!',
                    message=f'Congratulations! You won {participant.prize_won} coins in {participant.tournament.title}!',
                    link=f'/tournaments/{participant.tournament.pk}/'
                )
        
        self.message_user(request, f'Awarded prizes to {queryset.count()} participants')
    award_prize.short_description = 'Award prizes to selected participants'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Transaction admin"""
    list_display = ['user', 'transaction_type', 'amount', 'balance_after', 'created_at']
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['user__username', 'description']
    date_hierarchy = 'created_at'
    readonly_fields = ['user', 'transaction_type', 'amount', 'balance_after', 'created_at']


@admin.register(PaymentRequest)
class PaymentRequestAdmin(admin.ModelAdmin):
    """Payment request admin"""
    list_display = ['user', 'coins_amount', 'payment_amount', 'payment_method', 'status_badge', 'screenshot_preview', 'created_at', 'processed_by']
    list_filter = ['status', 'payment_method', 'created_at', 'processed_by']
    search_fields = ['user__username', 'transaction_id', 'user__email']
    date_hierarchy = 'created_at'
    list_per_page = 20
    
    fieldsets = (
        ('Request Details', {
            'fields': ('user', 'coins_amount', 'payment_amount', 'payment_method', 'transaction_id')
        }),
        ('Payment Proof', {
            'fields': ('payment_screenshot', 'screenshot_image_preview')
        }),
        ('Admin Actions', {
            'fields': ('status', 'admin_notes', 'processed_by', 'processed_at')
        }),
    )
    
    readonly_fields = ['user', 'created_at', 'screenshot_image_preview', 'processed_at']
    
    actions = ['approve_payment', 'reject_payment']
    
    def status_badge(self, obj):
        """Display status with color badge"""
        colors = {
            'pending': '#FFA500',
            'approved': '#10b981',
            'rejected': '#ef4444'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 12px; font-weight: bold;">{}</span>',
            colors.get(obj.status, '#6B7280'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def screenshot_preview(self, obj):
        """Display small preview of payment screenshot"""
        if obj.payment_screenshot:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 8px; border: 2px solid #e5e7eb;" /></a>',
                obj.payment_screenshot.url,
                obj.payment_screenshot.url
            )
        return '-'
    screenshot_preview.short_description = 'Screenshot'
    
    def screenshot_image_preview(self, obj):
        """Display full payment screenshot in detail view"""
        if obj.payment_screenshot:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="max-width: 500px; max-height: 500px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);" /></a><br><br><a href="{}" target="_blank" class="button">View Full Size</a>',
                obj.payment_screenshot.url,
                obj.payment_screenshot.url,
                obj.payment_screenshot.url
            )
        return 'No screenshot uploaded'
    screenshot_image_preview.short_description = 'Payment Screenshot'
    
    def approve_payment(self, request, queryset):
        """Approve selected payment requests"""
        for payment_req in queryset.filter(status='pending'):
            user = payment_req.user
            user.coins += payment_req.coins_amount
            user.save()
            
            Transaction.objects.create(
                user=user,
                transaction_type='deposit',
                amount=payment_req.coins_amount,
                description=f'Coins purchase via {payment_req.payment_method}',
                balance_after=user.coins
            )
            
            payment_req.status = 'approved'
            payment_req.processed_at = timezone.now()
            payment_req.processed_by = request.user
            payment_req.save()
            
            Notification.objects.create(
                user=user,
                notification_type='payment',
                title='Payment Approved',
                message=f'Your payment request for {payment_req.coins_amount} coins has been approved!',
                link='/wallet/'
            )
        
        self.message_user(request, f'Approved {queryset.count()} payment requests')
    approve_payment.short_description = 'Approve selected payment requests'
    
    def reject_payment(self, request, queryset):
        """Reject selected payment requests"""
        for payment_req in queryset.filter(status='pending'):
            payment_req.status = 'rejected'
            payment_req.processed_at = timezone.now()
            payment_req.processed_by = request.user
            payment_req.save()
            
            Notification.objects.create(
                user=payment_req.user,
                notification_type='payment',
                title='Payment Rejected',
                message=f'Your payment request for {payment_req.coins_amount} coins has been rejected. Please contact support.',
                link='/wallet/'
            )
        
        self.message_user(request, f'Rejected {queryset.count()} payment requests')
    reject_payment.short_description = 'Reject selected payment requests'


@admin.register(PaymentQR)
class PaymentQRAdmin(admin.ModelAdmin):
    """Payment QR admin"""
    list_display = ['payment_method', 'account_name', 'account_number', 'is_active']
    list_filter = ['payment_method', 'is_active']


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """Game category admin"""
    list_display = ['image_preview', 'name', 'slug', 'icon', 'banner_color_preview', 'display_order', 'is_active', 'item_count']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['display_order', 'is_active']
    ordering = ['display_order', 'name']
    
    def image_preview(self, obj):
        """Display image preview"""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 8px; border: 2px solid #e5e7eb;" />',
                obj.image.url
            )
        return '🎮'
    image_preview.short_description = 'Image'
    
    def banner_color_preview(self, obj):
        """Display banner color preview"""
        return format_html(
            '<div style="width: 40px; height: 20px; background: {}; border-radius: 4px; border: 1px solid #ccc;"></div>',
            obj.banner_color
        )
    banner_color_preview.short_description = 'Banner Color'
    
    def item_count(self, obj):
        """Display number of items in this game"""
        count = obj.items.count()
        return format_html(
            '<span style="font-weight: bold; color: #2563eb;">{} items</span>',
            count
        )
    item_count.short_description = 'Items'


@admin.register(StoreItem)
class StoreItemAdmin(admin.ModelAdmin):
    """Store item admin"""
    list_display = ['image_preview', 'name', 'game', 'quantity', 'price_display', 'featured', 'is_active', 'created_at']
    list_filter = ['game', 'featured', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['featured', 'is_active']
    list_per_page = 20
    
    fieldsets = (
        ('Item Details', {
            'fields': ('name', 'game', 'description', 'quantity', 'price')
        }),
        ('Image', {
            'fields': ('image', 'image_display')
        }),
        ('Display Options', {
            'fields': ('featured', 'is_active')
        }),
    )
    
    readonly_fields = ['image_display', 'created_at', 'updated_at']
    
    actions = ['mark_featured', 'mark_active', 'mark_inactive']
    
    def image_preview(self, obj):
        """Display small image preview in list"""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 8px; border: 2px solid #e5e7eb;" />',
                obj.image.url
            )
        return '📦'
    image_preview.short_description = 'Image'
    
    def image_display(self, obj):
        """Display full image in detail view"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 400px; max-height: 400px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);" />',
                obj.image.url
            )
        return 'No image uploaded'
    image_display.short_description = 'Item Image'
    
    def price_display(self, obj):
        """Display price with coin icon"""
        return format_html(
            '<span style="color: #0118D8; font-weight: bold;">💰 {} coins</span>',
            obj.price
        )
    price_display.short_description = 'Price'
    
    def featured_badge(self, obj):
        """Display featured status"""
        if obj.featured:
            return format_html('<span style="color: #f59e0b;">⭐ Featured</span>')
        return '-'
    featured_badge.short_description = 'Featured'
    
    def active_badge(self, obj):
        """Display active status with color"""
        if obj.is_active:
            return format_html('<span style="color: #10b981;">✓ Active</span>')
        return format_html('<span style="color: #ef4444;">✗ Inactive</span>')
    active_badge.short_description = 'Status'
    
    def mark_featured(self, request, queryset):
        """Mark items as featured"""
        queryset.update(featured=True)
        self.message_user(request, f'{queryset.count()} items marked as featured')
    mark_featured.short_description = 'Mark as featured'
    
    def mark_active(self, request, queryset):
        """Mark items as active"""
        queryset.update(is_active=True)
        self.message_user(request, f'{queryset.count()} items marked as active')
    mark_active.short_description = 'Mark as active'
    
    def mark_inactive(self, request, queryset):
        """Mark items as inactive"""
        queryset.update(is_active=False)
        self.message_user(request, f'{queryset.count()} items marked as inactive')
    mark_inactive.short_description = 'Mark as inactive'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Order admin"""
    list_display = ['order_id', 'user', 'item_display', 'total_price_display', 'in_game_id', 'status_badge', 'created_at']
    list_filter = ['status', 'created_at', 'item__game']
    search_fields = ['order_id', 'user__username', 'in_game_id', 'in_game_name', 'user__email']
    date_hierarchy = 'created_at'
    list_per_page = 20
    
    fieldsets = (
        ('Order Details', {
            'fields': ('order_id', 'user', 'item', 'item_image_preview', 'quantity', 'total_price')
        }),
        ('Delivery Information', {
            'fields': ('in_game_id', 'in_game_name')
        }),
        ('Status & Notes', {
            'fields': ('status', 'admin_notes', 'completed_at')
        }),
    )
    
    readonly_fields = ['order_id', 'user', 'item', 'total_price', 'created_at', 'item_image_preview', 'completed_at']
    
    actions = ['mark_processing', 'mark_completed', 'cancel_order']
    
    def status_badge(self, obj):
        """Display status with color badge"""
        colors = {
            'pending': '#FFA500',
            'processing': '#3b82f6',
            'completed': '#10b981',
            'cancelled': '#ef4444'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 12px; font-weight: bold;">{}</span>',
            colors.get(obj.status, '#6B7280'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def item_display(self, obj):
        """Display item with image"""
        if obj.item.image:
            return format_html(
                '<div style="display: flex; align-items: center; gap: 10px;"><img src="{}" style="width: 40px; height: 40px; object-fit: cover; border-radius: 6px;" /><span>{}</span></div>',
                obj.item.image.url,
                obj.item.name
            )
        return obj.item.name
    item_display.short_description = 'Item'
    
    def item_image_preview(self, obj):
        """Display item image in detail view"""
        if obj.item.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);" />',
                obj.item.image.url
            )
        return 'No image'
    item_image_preview.short_description = 'Item Image'
    
    def total_price_display(self, obj):
        """Display total price with coin icon"""
        return format_html(
            '<span style="color: #0118D8; font-weight: bold;">💰 {} coins</span>',
            obj.total_price
        )
    total_price_display.short_description = 'Total Price'
    
    def mark_processing(self, request, queryset):
        """Mark orders as processing"""
        queryset.update(status='processing')
        
        for order in queryset:
            Notification.objects.create(
                user=order.user,
                notification_type='order',
                title='Order Processing',
                message=f'Your order {order.order_id} is being processed.',
                link='/orders/'
            )
        
        self.message_user(request, f'Marked {queryset.count()} orders as processing')
    mark_processing.short_description = 'Mark as processing'
    
    def mark_completed(self, request, queryset):
        """Mark orders as completed"""
        queryset.update(status='completed', completed_at=timezone.now())
        
        for order in queryset:
            Notification.objects.create(
                user=order.user,
                notification_type='order',
                title='Order Completed',
                message=f'Your order {order.order_id} has been delivered to your game account!',
                link='/orders/'
            )
        
        self.message_user(request, f'Marked {queryset.count()} orders as completed')
    mark_completed.short_description = 'Mark as completed'
    
    def cancel_order(self, request, queryset):
        """Cancel orders and refund coins"""
        for order in queryset.filter(status__in=['pending', 'processing']):
            user = order.user
            user.coins += order.total_price
            user.save()
            
            Transaction.objects.create(
                user=user,
                transaction_type='admin_adjustment',
                amount=order.total_price,
                description=f'Refund for cancelled order: {order.order_id}',
                balance_after=user.coins
            )
            
            order.status = 'cancelled'
            order.save()
            
            Notification.objects.create(
                user=user,
                notification_type='order',
                title='Order Cancelled',
                message=f'Your order {order.order_id} has been cancelled. Coins have been refunded.',
                link='/orders/'
            )
        
        self.message_user(request, f'Cancelled {queryset.count()} orders and refunded coins')
    cancel_order.short_description = 'Cancel and refund'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Notification admin"""
    list_display = ['user', 'notification_type', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    date_hierarchy = 'created_at'


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    """Payment methods admin"""
    list_display = ['name', 'method_type', 'account_number', 'display_order', 'is_active_badge', 'created_at']
    list_filter = ['method_type', 'is_active']
    search_fields = ['name', 'account_number', 'account_name']
    list_editable = ['display_order']
    ordering = ['display_order', 'name']
    
    fieldsets = [
        ('Method Information', {
            'fields': ['name', 'method_type']
        }),
        ('Account Details', {
            'fields': ['account_number', 'account_name', 'qr_code']
        }),
        ('Instructions', {
            'fields': ['instructions']
        }),
        ('Display Settings', {
            'fields': ['display_order', 'is_active']
        }),
    ]
    
    def is_active_badge(self, obj):
        """Display active status as badge"""
        color = '#10b981' if obj.is_active else '#ef4444'
        status = 'Active' if obj.is_active else 'Inactive'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 12px; font-weight: bold;">{}</span>',
            color,
            status
        )
    is_active_badge.short_description = 'Status'
    
    actions = ['activate_methods', 'deactivate_methods']
    
    def activate_methods(self, request, queryset):
        """Activate selected payment methods"""
        queryset.update(is_active=True)
        self.message_user(request, f'{queryset.count()} payment methods activated')
    activate_methods.short_description = 'Activate selected methods'
    
    def deactivate_methods(self, request, queryset):
        """Deactivate selected payment methods"""
        queryset.update(is_active=False)
        self.message_user(request, f'{queryset.count()} payment methods deactivated')
    deactivate_methods.short_description = 'Deactivate selected methods'


class FullTournamentParticipantInline(admin.TabularInline):
    """Inline for full tournament participants"""
    model = FullTournamentParticipant
    extra = 0
    fields = ['user', 'gamer_tag', 'rank', 'kills', 'prize_won']


@admin.register(FullTournament)
class FullTournamentAdmin(admin.ModelAdmin):
    """Full tournament admin"""
    list_display = ['matchroom_id', 'title', 'game', 'team_type', 'status', 'current_participants', 'max_players', 'game_time']
    list_filter = ['game', 'team_type', 'status', 'game_time']
    search_fields = ['matchroom_id', 'title', 'game_map']
    date_hierarchy = 'game_time'
    inlines = [FullTournamentParticipantInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('matchroom_id', 'title', 'game', 'team_type')
        }),
        ('Tournament Details', {
            'fields': ('max_players', 'entry_fee', 'game_time', 'game_map', 'status')
        }),
        ('Prize Distribution', {
            'fields': ('first_place_prize', 'rank_2_5_prize', 'per_kill_prize')
        }),
        ('Room Information', {
            'fields': ('room_id', 'room_password')
        }),
        ('Rules', {
            'fields': ('rules_regulations',)
        }),
    )
    
    readonly_fields = ['matchroom_id']
    
    actions = ['start_tournament', 'complete_tournament']
    
    def start_tournament(self, request, queryset):
        """Start selected tournaments"""
        queryset.update(status='ongoing')
        self.message_user(request, f'Started {queryset.count()} tournaments')
    start_tournament.short_description = 'Start selected tournaments'
    
    def complete_tournament(self, request, queryset):
        """Complete selected tournaments"""
        queryset.update(status='completed')
        self.message_user(request, f'Completed {queryset.count()} tournaments')
    complete_tournament.short_description = 'Complete selected tournaments'


@admin.register(FullTournamentParticipant)
class FullTournamentParticipantAdmin(admin.ModelAdmin):
    """Full tournament participant admin"""
    list_display = ['user', 'tournament', 'gamer_tag', 'rank', 'kills', 'prize_won']
    list_filter = ['tournament__game', 'tournament']
    search_fields = ['user__username', 'gamer_tag', 'tournament__matchroom_id']
    
    fieldsets = (
        ('Participant Info', {
            'fields': ('tournament', 'user', 'gamer_tag')
        }),
        ('Results', {
            'fields': ('rank', 'kills', 'prize_won')
        }),
    )


# Customize admin site
admin.site.site_header = '🎮 Gaming Platform Admin Panel'
admin.site.site_title = 'Gaming Platform Admin'
admin.site.index_title = 'Dashboard - Manage Store, Payments & Orders'

# Custom admin dashboard text
admin.site.site_url = '/'  # Link to main site
