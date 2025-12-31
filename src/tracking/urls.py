from django.urls import path
from . import views


app_name = 'tracking'

urlpatterns = [
    # Spending views (keep original paths for compatibility with existing links)
    path('', views.spending_list_view, name='spending_list'),
    path('dashboard/', views.spending_dashboard_view, name='spending_dashboard'),
    path('create/', views.spending_create_view, name='spending_create'),
    path('<int:pk>/', views.spending_detail_view, name='spending_detail'),
    path('<int:pk>/edit/', views.spending_edit_view, name='spending_edit'),
    path('<int:pk>/delete/', views.spending_delete_view, name='spending_delete'),
    
    # Saving views
    path('saving/', views.saving_list_view, name='saving_list'),
    path('saving/dashboard/', views.saving_dashboard_view, name='saving_dashboard'),
    path('saving/create/', views.saving_create_view, name='saving_create'),
    path('saving/<int:pk>/', views.saving_detail_view, name='saving_detail'),
    path('saving/<int:pk>/edit/', views.saving_edit_view, name='saving_edit'),
    path('saving/<int:pk>/delete/', views.saving_delete_view, name='saving_delete'),
    
    # Saving Goal views
    path('saving-goal/', views.saving_goal_list_view, name='saving_goal_list'),
    path('saving-goal/create/', views.saving_goal_create_view, name='saving_goal_create'),
    path('saving-goal/<int:pk>/', views.saving_goal_detail_view, name='saving_goal_detail'),
    path('saving-goal/<int:pk>/edit/', views.saving_goal_edit_view, name='saving_goal_edit'),
    path('saving-goal/<int:pk>/delete/', views.saving_goal_delete_view, name='saving_goal_delete'),
]


