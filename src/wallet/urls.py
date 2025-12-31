from django.urls import path
from . import views


app_name = 'wallet'

urlpatterns = [
    # Wallet views
    path('', views.wallet_list_view, name='wallet_list'),
    path('dashboard/', views.wallet_dashboard_view, name='wallet_dashboard'),
    path('create/', views.wallet_create_view, name='wallet_create'),
    path('<int:pk>/', views.wallet_detail_view, name='wallet_detail'),
    path('<int:pk>/edit/', views.wallet_edit_view, name='wallet_edit'),
    path('<int:pk>/delete/', views.wallet_delete_view, name='wallet_delete'),
    
    # Transaction views
    path('<int:wallet_pk>/transactions/', views.transaction_list_view, name='transaction_list'),
    path('<int:wallet_pk>/transactions/create/', views.transaction_create_view, name='transaction_create'),
    path('transactions/<int:pk>/', views.transaction_detail_view, name='transaction_detail'),
    path('transactions/<int:pk>/edit/', views.transaction_edit_view, name='transaction_edit'),
    path('transactions/<int:pk>/delete/', views.transaction_delete_view, name='transaction_delete'),
]




