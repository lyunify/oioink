from django.urls import path
from . import views

app_name = 'prizes'

urlpatterns = [
    path('', views.prize_list_view, name='prize_list'),
    path('<int:pk>/', views.prize_detail_view, name='prize_detail'),
    path('<int:pk>/redeem/', views.prize_redeem_view, name='prize_redeem'),
    path('my-prizes/', views.my_prizes_view, name='my_prizes'),
]




