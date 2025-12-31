from django.urls import path
from . import views


app_name = 'achievements'

urlpatterns = [
    path('', views.achievement_list_view, name='achievement_list'),
    path('my/', views.my_achievements_view, name='my_achievements'),
    path('<int:pk>/', views.achievement_detail_view, name='achievement_detail'),
    path('api/unnotified/', views.get_unnotified_achievements_view, name='get_unnotified_achievements'),
    path('api/<int:pk>/mark-notified/', views.mark_achievement_notified_view, name='mark_achievement_notified'),
]

