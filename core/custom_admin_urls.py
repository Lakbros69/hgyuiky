"""
Custom Admin Panel URLs
"""
from django.urls import path
from . import custom_admin_views as views

app_name = 'custom_admin'

urlpatterns = [
    # Dashboard
    path('', views.custom_admin_dashboard, name='dashboard'),
    
    # Payment Management
    path('payments/', views.payment_management, name='payments'),
    path('payments/<int:payment_id>/approve/', views.approve_payment, name='approve_payment'),
    path('payments/<int:payment_id>/reject/', views.reject_payment, name='reject_payment'),
    
    # Order Management
    path('orders/', views.order_management, name='orders'),
    path('orders/<int:order_id>/update/', views.update_order_status, name='update_order'),
    
    # Store Management
    path('store/', views.store_management, name='store'),
    path('store/add/', views.add_store_item, name='add_item'),
    path('store/<int:item_id>/edit/', views.edit_store_item, name='edit_item'),
    path('store/<int:item_id>/toggle/', views.toggle_item_status, name='toggle_item'),
    
    # User Management
    path('users/', views.user_management, name='users'),
    path('users/<int:user_id>/add-coins/', views.add_coins, name='add_coins'),
    
    # Payment Methods Management
    path('payment-methods/', views.payment_methods, name='payment_methods'),
    path('payment-methods/add/', views.add_payment_method, name='add_payment_method'),
    path('payment-methods/<int:method_id>/edit/', views.edit_payment_method, name='edit_payment_method'),
    path('payment-methods/<int:method_id>/toggle/', views.toggle_payment_method, name='toggle_payment_method'),
    path('payment-methods/<int:method_id>/delete/', views.delete_payment_method, name='delete_payment_method'),
    
    # Game Categories Management
    path('games/', views.game_management, name='games'),
    path('games/add/', views.add_game, name='add_game'),
    path('games/<int:game_id>/edit/', views.edit_game, name='edit_game'),
    path('games/<int:game_id>/toggle/', views.toggle_game_status, name='toggle_game'),
    path('games/<int:game_id>/delete/', views.delete_game, name='delete_game'),
    
    # Full Tournament Management
    path('tournaments/', views.full_tournaments, name='full_tournaments'),
    path('tournaments/create/', views.create_full_tournament, name='create_full_tournament'),
    path('tournaments/<int:tournament_id>/set-room/', views.set_full_tournament_room, name='set_full_tournament_room'),
    path('tournaments/<int:tournament_id>/finish/', views.finish_full_tournament, name='finish_full_tournament'),
    path('tournaments/<int:tournament_id>/delete/', views.delete_full_tournament, name='delete_full_tournament'),
    
    # Withdrawal Management
    path('withdrawals/', views.withdrawal_management, name='withdrawals'),
    path('withdrawals/<int:withdrawal_id>/process/', views.process_withdrawal, name='process_withdrawal'),
    
    # Chat Management
    path('chat/', views.chat_management, name='chat_management'),
    path('chat/<int:chat_id>/', views.chat_detail, name='chat_detail'),
    
    # Website Settings
    path('settings/', views.website_settings, name='settings'),
]
