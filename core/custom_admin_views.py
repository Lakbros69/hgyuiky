"""
Custom Admin Panel Views
Separate from Django admin - for website customization
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from django.forms import modelformset_factory
from datetime import timedelta

from .models import (
    User, Tournament, StoreItem, Order, PaymentRequest,
    Transaction, Notification, PaymentMethod, Game, FullTournament,
    SliderImage, WithdrawalRequest, ChatMessage
)
from .forms import SliderImageForm


@staff_member_required
def custom_admin_dashboard(request):
    """Main admin dashboard with statistics"""
    
    # Get statistics
    total_users = User.objects.count()
    total_tournaments = Tournament.objects.count()
    active_tournaments = Tournament.objects.filter(status='ongoing').count()
    
    pending_payments = PaymentRequest.objects.filter(status='pending').count()
    pending_orders = Order.objects.filter(status='pending').count()
    
    total_revenue = PaymentRequest.objects.filter(
        status='approved'
    ).aggregate(total=Sum('payment_amount'))['total'] or 0
    
    # Recent activity
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_payments = PaymentRequest.objects.order_by('-created_at')[:5]
    recent_orders = Order.objects.order_by('-created_at')[:5]
    
    # This week stats
    week_ago = timezone.now() - timedelta(days=7)
    new_users_week = User.objects.filter(date_joined__gte=week_ago).count()
    payments_week = PaymentRequest.objects.filter(
        created_at__gte=week_ago,
        status='approved'
    ).count()
    
    context = {
        'total_users': total_users,
        'total_tournaments': total_tournaments,
        'active_tournaments': active_tournaments,
        'pending_payments': pending_payments,
        'pending_orders': pending_orders,
        'total_revenue': total_revenue,
        'recent_users': recent_users,
        'recent_payments': recent_payments,
        'recent_orders': recent_orders,
        'new_users_week': new_users_week,
        'payments_week': payments_week,
    }
    
    return render(request, 'custom_admin/dashboard.html', context)


@staff_member_required
def payment_management(request):
    """Manage payment requests"""
    status_filter = request.GET.get('status', 'pending')
    
    payments = PaymentRequest.objects.filter(status=status_filter).order_by('-created_at')
    
    context = {
        'payments': payments,
        'status_filter': status_filter,
        'pending_count': PaymentRequest.objects.filter(status='pending').count(),
    }
    
    return render(request, 'custom_admin/payments.html', context)


@staff_member_required
def approve_payment(request, payment_id):
    """Approve a payment request"""
    payment = get_object_or_404(PaymentRequest, id=payment_id)
    
    if payment.status == 'pending':
        user = payment.user
        user.coins += payment.coins_amount
        user.save()
        
        Transaction.objects.create(
            user=user,
            transaction_type='deposit',
            amount=payment.coins_amount,
            description=f'Coins purchase via {payment.payment_method}',
            balance_after=user.coins
        )
        
        payment.status = 'approved'
        payment.processed_at = timezone.now()
        payment.processed_by = request.user
        payment.save()
        
        Notification.objects.create(
            user=user,
            notification_type='payment',
            title='Payment Approved',
            message=f'Your payment request for {payment.coins_amount} coins has been approved!',
            link='/wallet/'
        )
        
        messages.success(request, f'Payment approved! {payment.coins_amount} coins added to {user.username}')
    
    return redirect('custom_admin:payments')


@staff_member_required
def reject_payment(request, payment_id):
    """Reject a payment request"""
    payment = get_object_or_404(PaymentRequest, id=payment_id)
    
    if payment.status == 'pending':
        payment.status = 'rejected'
        payment.processed_at = timezone.now()
        payment.processed_by = request.user
        payment.save()
        
        Notification.objects.create(
            user=payment.user,
            notification_type='payment',
            title='Payment Rejected',
            message=f'Your payment request for {payment.coins_amount} coins has been rejected. Please contact support.',
            link='/wallet/'
        )
        
        messages.warning(request, f'Payment rejected for {payment.user.username}')
    
    return redirect('custom_admin:payments')


@staff_member_required
def order_management(request):
    """Manage orders"""
    status_filter = request.GET.get('status', 'pending')
    
    orders = Order.objects.filter(status=status_filter).select_related(
        'user', 'item'
    ).order_by('-created_at')
    
    context = {
        'orders': orders,
        'status_filter': status_filter,
        'pending_count': Order.objects.filter(status='pending').count(),
    }
    
    return render(request, 'custom_admin/orders.html', context)


@staff_member_required
def update_order_status(request, order_id):
    """Update order status"""
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        admin_notes = request.POST.get('admin_notes', '')
        
        if new_status in ['processing', 'completed', 'cancelled']:
            order.status = new_status
            if admin_notes:
                order.admin_notes = admin_notes
            
            if new_status == 'completed':
                order.completed_at = timezone.now()
            
            order.save()
            
            # Create notification
            status_messages = {
                'processing': 'Your order is being processed.',
                'completed': 'Your order has been delivered to your game account!',
                'cancelled': 'Your order has been cancelled. Coins have been refunded.'
            }
            
            Notification.objects.create(
                user=order.user,
                notification_type='order',
                title=f'Order {order.status.title()}',
                message=status_messages.get(new_status, 'Order status updated'),
                link='/orders/'
            )
            
            # Refund if cancelled
            if new_status == 'cancelled':
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
            
            messages.success(request, f'Order {order.order_id} updated to {new_status}')
        
    return redirect('custom_admin:orders')


@staff_member_required
def store_management(request):
    """Manage store items with game categories"""
    # Get all games dynamically from database
    games = Game.objects.all().prefetch_related('items')
    
    game_categories = {}
    for game in games:
        game_categories[game.slug] = {
            'name': game.name,
            'title': f'{game.name.upper()} PRODUCTS',
            'types': game.get_product_types_list(),
            'items': game.items.all().order_by('-created_at'),
            'url_param': game.slug,
            'icon': game.icon,
            'image': game.image.url if game.image else None,
            'total': game.items.count(),
            'active': game.items.filter(is_active=True).count(),
        }
    
    context = {
        'game_categories': game_categories,
        'total_items': StoreItem.objects.count(),
        'active_count': StoreItem.objects.filter(is_active=True).count(),
    }
    
    return render(request, 'custom_admin/store.html', context)


@staff_member_required
def add_store_item(request):
    """Add new store item"""
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            game_id = request.POST.get('game')
            game = get_object_or_404(Game, id=game_id)
            price = int(request.POST.get('price'))
            image = request.FILES.get('image')
            
            # Set default values for fields not in the form
            description = name  # Use name as description
            quantity = 1  # Default quantity
            featured = False
            is_active = True  # Active by default
            
            StoreItem.objects.create(
                name=name,
                game=game,
                description=description,
                quantity=quantity,
                price=price,
                image=image,
                featured=featured,
                is_active=is_active
            )
            
            messages.success(request, f'Store item "{name}" created successfully!')
            return redirect('custom_admin:store')
            
        except Exception as e:
            messages.error(request, f'Error creating item: {str(e)}')
    
    context = {
        'games': Game.objects.filter(is_active=True)
    }
    
    return render(request, 'custom_admin/add_store_item.html', context)


@staff_member_required
def edit_store_item(request, item_id):
    """Edit store item"""
    item = get_object_or_404(StoreItem, id=item_id)
    
    if request.method == 'POST':
        try:
            item.name = request.POST.get('name')
            game_id = request.POST.get('game')
            item.game = get_object_or_404(Game, id=game_id)
            item.price = int(request.POST.get('price'))
            
            # Update description if name changed
            item.description = item.name
            
            if request.FILES.get('image'):
                item.image = request.FILES.get('image')
            
            item.save()
            
            messages.success(request, f'Store item "{item.name}" updated successfully!')
            return redirect('custom_admin:store')
            
        except Exception as e:
            messages.error(request, f'Error updating item: {str(e)}')
    
    context = {
        'item': item,
        'games': Game.objects.all()
    }
    
    return render(request, 'custom_admin/edit_store_item.html', context)


@staff_member_required
def toggle_item_status(request, item_id):
    """Toggle store item active status"""
    item = get_object_or_404(StoreItem, id=item_id)
    item.is_active = not item.is_active
    item.save()
    
    status = 'activated' if item.is_active else 'deactivated'
    messages.success(request, f'{item.name} has been {status}')
    
    return redirect('custom_admin:store')


@staff_member_required
def website_settings(request):
    """Website customization settings"""
    # Ensure three default slider positions exist
    default_slides = [
        {
            'title': 'Epic Gaming Tournaments',
            'subtitle': 'Join the biggest gaming competitions',
        },
        {
            'title': 'Win Amazing Prizes',
            'subtitle': 'Compete and earn exclusive rewards',
        },
        {
            'title': 'Join The Community',
            'subtitle': 'Connect with gamers worldwide',
        },
    ]

    for index, defaults in enumerate(default_slides, start=1):
        SliderImage.objects.get_or_create(position=index, defaults=defaults)

    slider_queryset = SliderImage.objects.order_by('position')
    SliderImageFormSet = modelformset_factory(
        SliderImage,
        form=SliderImageForm,
        extra=0,
        can_delete=False
    )
    slider_formset = SliderImageFormSet(queryset=slider_queryset)

    if request.method == 'POST':
        section = request.POST.get('section')

        if section == 'slider':
            slider_formset = SliderImageFormSet(
                request.POST,
                request.FILES,
                queryset=slider_queryset
            )

            if slider_formset.is_valid():
                slider_formset.save()
                messages.success(request, 'Slider images updated successfully!')
                return redirect('custom_admin:settings')

            messages.error(request, 'Please correct the errors below and try again.')
        else:
            # Placeholder success for other sections until fully implemented
            messages.success(request, 'Settings updated successfully!')
            return redirect('custom_admin:settings')

    context = {
        'slider_formset': slider_formset,
    }

    return render(request, 'custom_admin/settings.html', context)


@staff_member_required
def user_management(request):
    """Manage users"""
    search = request.GET.get('search', '')
    
    users = User.objects.all()
    if search:
        users = users.filter(username__icontains=search) | users.filter(email__icontains=search)
    
    users = users.order_by('-date_joined')[:50]
    
    context = {
        'users': users,
        'total_users': User.objects.count(),
        'search': search,
    }
    
    return render(request, 'custom_admin/users.html', context)


@staff_member_required
def add_coins(request, user_id):
    """Add coins to a user"""
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        amount = int(request.POST.get('amount', 0))
        reason = request.POST.get('reason', 'Admin adjustment')
        
        if amount > 0:
            user.coins += amount
            user.save()
            
            Transaction.objects.create(
                user=user,
                transaction_type='admin_adjustment',
                amount=amount,
                description=reason,
                balance_after=user.coins
            )
            
            Notification.objects.create(
                user=user,
                notification_type='system',
                title='Coins Added',
                message=f'{amount} coins have been added to your account!',
                link='/wallet/'
            )
            
            messages.success(request, f'{amount} coins added to {user.username}')
    
    return redirect('custom_admin:users')


@staff_member_required
def payment_methods(request):
    """Manage payment methods"""
    methods = PaymentMethod.objects.all()
    
    context = {
        'methods': methods,
        'active_count': PaymentMethod.objects.filter(is_active=True).count(),
    }
    
    return render(request, 'custom_admin/payment_methods.html', context)


@staff_member_required
def add_payment_method(request):
    """Add new payment method"""
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            method_type = request.POST.get('method_type')
            account_number = request.POST.get('account_number', '')
            account_name = request.POST.get('account_name', '')
            instructions = request.POST.get('instructions', '')
            display_order = int(request.POST.get('display_order', 0))
            qr_code = request.FILES.get('qr_code')
            is_active = request.POST.get('is_active') == 'on'
            
            PaymentMethod.objects.create(
                name=name,
                method_type=method_type,
                account_number=account_number,
                account_name=account_name,
                instructions=instructions,
                display_order=display_order,
                qr_code=qr_code,
                is_active=is_active
            )
            
            messages.success(request, f'Payment method "{name}" created successfully!')
            return redirect('custom_admin:payment_methods')
            
        except Exception as e:
            messages.error(request, f'Error creating payment method: {str(e)}')
    
    context = {
        'method_types': PaymentMethod.METHOD_TYPES
    }
    
    return render(request, 'custom_admin/add_payment_method.html', context)


@staff_member_required
def edit_payment_method(request, method_id):
    """Edit payment method"""
    method = get_object_or_404(PaymentMethod, id=method_id)
    
    if request.method == 'POST':
        try:
            method.name = request.POST.get('name')
            method.method_type = request.POST.get('method_type')
            method.account_number = request.POST.get('account_number', '')
            method.account_name = request.POST.get('account_name', '')
            method.instructions = request.POST.get('instructions', '')
            method.display_order = int(request.POST.get('display_order', 0))
            method.is_active = request.POST.get('is_active') == 'on'
            
            if request.FILES.get('qr_code'):
                method.qr_code = request.FILES.get('qr_code')
            
            method.save()
            
            messages.success(request, f'Payment method "{method.name}" updated successfully!')
            return redirect('custom_admin:payment_methods')
            
        except Exception as e:
            messages.error(request, f'Error updating payment method: {str(e)}')
    
    context = {
        'method': method,
        'method_types': PaymentMethod.METHOD_TYPES
    }
    
    return render(request, 'custom_admin/edit_payment_method.html', context)


@staff_member_required
def toggle_payment_method(request, method_id):
    """Toggle payment method active status"""
    method = get_object_or_404(PaymentMethod, id=method_id)
    method.is_active = not method.is_active
    method.save()
    
    status = 'activated' if method.is_active else 'deactivated'
    messages.success(request, f'{method.name} has been {status}')
    
    return redirect('custom_admin:payment_methods')


@staff_member_required
def delete_payment_method(request, method_id):
    """Delete payment method"""
    method = get_object_or_404(PaymentMethod, id=method_id)
    name = method.name
    method.delete()
    
    messages.success(request, f'Payment method "{name}" has been deleted')
    return redirect('custom_admin:payment_methods')


# Game Management Views
@staff_member_required
def game_management(request):
    """Manage game categories"""
    games = Game.objects.all().annotate(
        item_count=Count('items'),
        active_items=Count('items', filter=Q(items__is_active=True))
    )
    
    context = {
        'games': games,
        'total_games': games.count(),
        'active_games': Game.objects.filter(is_active=True).count(),
    }
    
    return render(request, 'custom_admin/games.html', context)


@staff_member_required
def add_game(request):
    """Add new game category"""
    if request.method == 'POST':
        try:
            from django.utils.text import slugify
            
            name = request.POST.get('name')
            slug = slugify(request.POST.get('slug') or name)
            icon = request.POST.get('icon', 'gamepad')
            image = request.FILES.get('image')
            banner_color = request.POST.get('banner_color', '#2c3e6d')
            description = request.POST.get('description', '')
            product_types = request.POST.get('product_types')
            order_summary_note = request.POST.get('order_summary_note', '')
            order_id_label = request.POST.get('order_id_label', '')
            order_id_placeholder = request.POST.get('order_id_placeholder', '')
            order_id_help_text = request.POST.get('order_id_help_text', '')
            order_name_label = request.POST.get('order_name_label', '')
            order_name_placeholder = request.POST.get('order_name_placeholder', '')
            order_name_help_text = request.POST.get('order_name_help_text', '')
            display_order = int(request.POST.get('display_order', 0))
            is_active = request.POST.get('is_active') == 'on'
            
            Game.objects.create(
                name=name,
                slug=slug,
                icon=icon,
                image=image,
                banner_color=banner_color,
                description=description,
                product_types=product_types,
                order_summary_note=order_summary_note,
                order_id_label=order_id_label,
                order_id_placeholder=order_id_placeholder,
                order_id_help_text=order_id_help_text,
                order_name_label=order_name_label,
                order_name_placeholder=order_name_placeholder,
                order_name_help_text=order_name_help_text,
                display_order=display_order,
                is_active=is_active
            )
            
            messages.success(request, f'Game category "{name}" created successfully!')
            return redirect('custom_admin:games')
            
        except Exception as e:
            messages.error(request, f'Error creating game: {str(e)}')
    
    return render(request, 'custom_admin/add_game.html')


@staff_member_required
def edit_game(request, game_id):
    """Edit game category"""
    game = get_object_or_404(Game, id=game_id)
    
    if request.method == 'POST':
        try:
            from django.utils.text import slugify
            
            game.name = request.POST.get('name')
            game.slug = slugify(request.POST.get('slug') or game.name)
            game.icon = request.POST.get('icon', 'gamepad')
            
            if request.FILES.get('image'):
                game.image = request.FILES.get('image')
                
            game.banner_color = request.POST.get('banner_color', '#2c3e6d')
            game.description = request.POST.get('description', '')
            game.product_types = request.POST.get('product_types')
            game.order_summary_note = request.POST.get('order_summary_note', '')
            game.order_id_label = request.POST.get('order_id_label', '')
            game.order_id_placeholder = request.POST.get('order_id_placeholder', '')
            game.order_id_help_text = request.POST.get('order_id_help_text', '')
            game.order_name_label = request.POST.get('order_name_label', '')
            game.order_name_placeholder = request.POST.get('order_name_placeholder', '')
            game.order_name_help_text = request.POST.get('order_name_help_text', '')
            game.display_order = int(request.POST.get('display_order', 0))
            game.is_active = request.POST.get('is_active') == 'on'
            game.save()
            
            messages.success(request, f'Game category "{game.name}" updated successfully!')
            return redirect('custom_admin:games')
            
        except Exception as e:
            messages.error(request, f'Error updating game: {str(e)}')
    
    context = {
        'game': game,
    }
    
    return render(request, 'custom_admin/edit_game.html', context)


@staff_member_required
def toggle_game_status(request, game_id):
    """Toggle game active status"""
    game = get_object_or_404(Game, id=game_id)
    game.is_active = not game.is_active
    game.save()
    
    status = 'activated' if game.is_active else 'deactivated'
    messages.success(request, f'{game.name} has been {status}')
    
    return redirect('custom_admin:games')


@staff_member_required
def delete_game(request, game_id):
    """Delete game category"""
    game = get_object_or_404(Game, id=game_id)
    name = game.name
    
    # Check if game has items
    item_count = game.items.count()
    if item_count > 0:
        messages.error(request, f'Cannot delete "{name}" because it has {item_count} store items. Delete the items first.')
        return redirect('custom_admin:games')
    
    game.delete()
    messages.success(request, f'Game category "{name}" has been deleted')
    return redirect('custom_admin:games')


@staff_member_required
def full_tournaments(request):
    """List all full map tournaments"""
    tournaments = FullTournament.objects.all().order_by('-created_at')
    
    context = {
        'tournaments': tournaments,
    }
    return render(request, 'custom_admin/full_tournaments.html', context)


@staff_member_required
def set_full_tournament_room(request, tournament_id):
    """Set room details for full tournament"""
    tournament = get_object_or_404(FullTournament, pk=tournament_id)
    
    # Check if it's within 5 minutes of game time
    time_until_match = tournament.game_time - timezone.now()
    if time_until_match.total_seconds() > 300:  # More than 5 minutes
        messages.error(request, 'Room details can only be set within 5 minutes of the match start time.')
        return redirect('custom_admin:full_tournaments')
    
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        room_password = request.POST.get('room_password')
        
        if room_id and room_password:
            tournament.room_id = room_id
            tournament.room_password = room_password
            tournament.room_id_set_at = timezone.now()
            tournament.save()
            
            # Notify all participants
            for participant in tournament.full_participants.all():
                Notification.objects.create(
                    user=participant.user,
                    title='Room Details Available',
                    message=f'Room details for "{tournament.title}" are now available. Room ID: {room_id}, Password: {room_password}',
                    notification_type='tournament'
                )
            
            messages.success(request, 'Room details set successfully and participants notified.')
            return redirect('custom_admin:full_tournaments')
        else:
            messages.error(request, 'Both Room ID and Password are required.')
    
    context = {
        'tournament': tournament,
        'time_until_match': time_until_match,
    }
    return render(request, 'custom_admin/set_full_tournament_room.html', context)


@staff_member_required
def finish_full_tournament(request, tournament_id):
    """Finish a full tournament and allow result entry"""
    tournament = get_object_or_404(FullTournament, pk=tournament_id)
    
    # Check if tournament has started
    if tournament.game_time > timezone.now():
        messages.error(request, 'Tournament has not started yet.')
        return redirect('custom_admin:full_tournaments')
    
    if tournament.status == 'completed':
        messages.warning(request, 'Tournament is already completed.')
        return redirect('custom_admin:full_tournaments')
    
    # Update tournament status
    tournament.status = 'completed'
    tournament.save()
    
    # Notify all participants that they can submit results
    for participant in tournament.full_participants.all():
        Notification.objects.create(
            user=participant.user,
            title='Tournament Finished',
            message=f'"{tournament.title}" has finished. You can now submit your results.',
            notification_type='tournament'
        )
    
    messages.success(request, 'Tournament marked as finished. Participants can now submit results.')
    return redirect('custom_admin:full_tournaments')


@staff_member_required
def delete_full_tournament(request, tournament_id):
    """Delete a full tournament and refund participants"""
    tournament = get_object_or_404(FullTournament, pk=tournament_id)
    
    if request.method == 'POST':
        tournament_title = tournament.title
        
        # Refund all participants
        for participant in tournament.full_participants.all():
            if tournament.entry_fee > 0:
                participant.user.coins += tournament.entry_fee
                participant.user.save()
                
                # Record refund transaction
                Transaction.objects.create(
                    user=participant.user,
                    transaction_type='refund',
                    amount=tournament.entry_fee,
                    description=f'Refund for deleted tournament: {tournament_title}',
                    balance_after=participant.user.coins
                )
            
            # Notify participant
            Notification.objects.create(
                user=participant.user,
                title='Tournament Cancelled',
                message=f'Tournament "{tournament_title}" has been cancelled by admin. Your entry fee has been refunded.',
                notification_type='tournament'
            )
        
        # Delete the tournament
        tournament.delete()
        
    messages.success(request, f'Tournament "{tournament_title}" has been deleted and all participants refunded.')
    return redirect('custom_admin:full_tournaments')


@staff_member_required
def withdrawal_management(request):
    """Manage withdrawal requests"""
    status_filter = request.GET.get('status', 'all')
    search = request.GET.get('search', '')
    
    withdrawals = WithdrawalRequest.objects.all().select_related('user', 'processed_by')
    
    if status_filter != 'all':
        withdrawals = withdrawals.filter(status=status_filter)
    
    if search:
        withdrawals = withdrawals.filter(
            Q(user__username__icontains=search) |
            Q(user__email__icontains=search) |
            Q(payment_method__icontains=search)
        )
    
    withdrawals = withdrawals.order_by('-created_at')
    
    # Statistics
    total_withdrawals = WithdrawalRequest.objects.count()
    pending_withdrawals = WithdrawalRequest.objects.filter(status='pending').count()
    approved_withdrawals = WithdrawalRequest.objects.filter(status='approved').count()
    rejected_withdrawals = WithdrawalRequest.objects.filter(status='rejected').count()
    
    total_amount_pending = WithdrawalRequest.objects.filter(status='pending').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    total_amount_approved = WithdrawalRequest.objects.filter(status='approved').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    context = {
        'withdrawals': withdrawals,
        'status_filter': status_filter,
        'search': search,
        'total_withdrawals': total_withdrawals,
        'pending_withdrawals': pending_withdrawals,
        'approved_withdrawals': approved_withdrawals,
        'rejected_withdrawals': rejected_withdrawals,
        'total_amount_pending': total_amount_pending,
        'total_amount_approved': total_amount_approved,
    }
    
    return render(request, 'custom_admin/withdrawals.html', context)


@staff_member_required
def process_withdrawal(request, withdrawal_id):
    """Process a withdrawal request (approve/reject)"""
    withdrawal = get_object_or_404(WithdrawalRequest, pk=withdrawal_id)
    
    if withdrawal.status != 'pending':
        messages.error(request, 'This withdrawal request has already been processed.')
        return redirect('custom_admin:withdrawals')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        admin_notes = request.POST.get('admin_notes', '')
        
        if action == 'approve':
            withdrawal.status = 'approved'
            withdrawal.admin_notes = admin_notes
            withdrawal.processed_at = timezone.now()
            withdrawal.processed_by = request.user
            withdrawal.save()
            
            # Create notification for user
            Notification.objects.create(
                user=withdrawal.user,
                title='Withdrawal Approved',
                message=f'Your withdrawal request for {withdrawal.amount} points has been approved and processed.',
                notification_type='system'
            )
            
            messages.success(request, f'Withdrawal request for {withdrawal.amount} points approved successfully.')
            
        elif action == 'reject':
            withdrawal.status = 'rejected'
            withdrawal.admin_notes = admin_notes
            withdrawal.processed_at = timezone.now()
            withdrawal.processed_by = request.user
            withdrawal.save()
            
            # Refund points to user
            withdrawal.user.coins += withdrawal.amount
            withdrawal.user.save()
            
            # Create refund transaction
            Transaction.objects.create(
                user=withdrawal.user,
                transaction_type='refund',
                amount=withdrawal.amount,
                description=f'Refund for rejected withdrawal request #{withdrawal.id}',
                balance_after=withdrawal.user.coins
            )
            
            # Create notification for user
            Notification.objects.create(
                user=withdrawal.user,
                title='Withdrawal Rejected',
                message=f'Your withdrawal request for {withdrawal.amount} points has been rejected. Points have been refunded to your account.',
                notification_type='system'
            )
            
            messages.success(request, f'Withdrawal request rejected and {withdrawal.amount} points refunded to user.')
        
        return redirect('custom_admin:withdrawals')
    
    context = {
        'withdrawal': withdrawal,
    }
    return render(request, 'custom_admin/process_withdrawal.html', context)


@staff_member_required
def create_full_tournament(request):
    """Create new full map tournament"""
    if request.method == 'POST':
        try:
            from datetime import datetime
            
            # Get form data
            title = request.POST.get('title')
            game = request.POST.get('game')
            team_type = request.POST.get('team_type')
            max_players = int(request.POST.get('max_players', 100))
            entry_fee = int(request.POST.get('entry_fee', 0))
            
            # Parse game date and time
            game_date = request.POST.get('game_date')
            game_time = request.POST.get('game_time')
            game_datetime = datetime.strptime(f"{game_date} {game_time}", "%Y-%m-%d %H:%M")
            
            game_map = request.POST.get('game_map')
            
            # Prize distribution
            first_place_prize = int(request.POST.get('first_place_prize'))
            rank_2_5_prize = int(request.POST.get('rank_2_5_prize'))
            per_kill_prize = int(request.POST.get('per_kill_prize'))
            
            rules_regulations = request.POST.get('rules_regulations')
            
            # Create tournament
            tournament = FullTournament.objects.create(
                title=title,
                game=game,
                team_type=team_type,
                max_players=max_players,
                entry_fee=entry_fee,
                game_time=game_datetime,
                game_map=game_map,
                first_place_prize=first_place_prize,
                rank_2_5_prize=rank_2_5_prize,
                per_kill_prize=per_kill_prize,
                rules_regulations=rules_regulations,
                created_by=request.user
            )
            
            messages.success(request, f'Full Tournament "{tournament.matchroom_id}" created successfully!')
            return redirect('custom_admin:full_tournaments')
            
        except Exception as e:
            messages.error(request, f'Error creating tournament: {str(e)}')
    
    context = {
        'game_choices': FullTournament.GAME_CHOICES,
        'team_choices': FullTournament.TEAM_CHOICES,
    }
    return render(request, 'custom_admin/create_full_tournament.html', context)


@staff_member_required
def chat_management(request):
    """Manage chat messages from users"""
    status_filter = request.GET.get('status', 'all')
    search = request.GET.get('search', '')
    
    chats = ChatMessage.objects.all().select_related('user', 'replied_by').order_by('-created_at')
    
    if status_filter != 'all':
        chats = chats.filter(status=status_filter)
    
    if search:
        chats = chats.filter(
            Q(user__username__icontains=search) |
            Q(user__email__icontains=search) |
            Q(subject__icontains=search) |
            Q(message__icontains=search)
        )
    
    # Statistics
    total_chats = ChatMessage.objects.count()
    new_chats = ChatMessage.objects.filter(status='new').count()
    read_chats = ChatMessage.objects.filter(status='read').count()
    replied_chats = ChatMessage.objects.filter(status='replied').count()
    resolved_chats = ChatMessage.objects.filter(status='resolved').count()
    
    context = {
        'chats': chats,
        'status_filter': status_filter,
        'search': search,
        'total_chats': total_chats,
        'new_chats': new_chats,
        'read_chats': read_chats,
        'replied_chats': replied_chats,
        'resolved_chats': resolved_chats,
    }
    return render(request, 'custom_admin/chat_management.html', context)


@staff_member_required
def chat_detail(request, chat_id):
    """View and reply to a chat message"""
    chat = get_object_or_404(ChatMessage, pk=chat_id)
    
    # Mark as read if it's new
    if chat.status == 'new':
        chat.status = 'read'
        chat.save()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        admin_reply = request.POST.get('admin_reply', '').strip()
        
        if action == 'reply' and admin_reply:
            chat.admin_reply = admin_reply
            chat.status = 'replied'
            chat.replied_by = request.user
            chat.replied_at = timezone.now()
            chat.save()
            
            # Create notification for user
            Notification.objects.create(
                user=chat.user,
                title='Reply to Your Message',
                message=f'We have replied to your message: "{chat.subject}". Check your chat for details.',
                notification_type='system'
            )
            
            messages.success(request, 'Reply sent successfully!')
            return redirect('custom_admin:chat_detail', chat_id=chat.id)
        
        elif action == 'resolve':
            chat.status = 'resolved'
            chat.save()
            messages.success(request, 'Chat marked as resolved.')
            return redirect('custom_admin:chat_management')
        
        elif action == 'mark_read':
            chat.status = 'read'
            chat.save()
            messages.success(request, 'Chat marked as read.')
            return redirect('custom_admin:chat_detail', chat_id=chat.id)
    
    context = {
        'chat': chat,
    }
    return render(request, 'custom_admin/chat_detail.html', context)
