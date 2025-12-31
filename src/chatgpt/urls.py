from django.urls import path
from django.contrib.auth import views
from . import views


app_name = 'chatgpt'

urlpatterns = [
    # get chatgpt
    path('get_chatgpt/', views.get_chatgpt_view, name='get_chatgpt'),
    # regen chatgpt
    path('regen_chatgpt/', views.regen_chatgpt_view, name='regen_chatgpt'),
    # chatgpt list
    path('chatgpt_list/', views.chatgpt_list_view, name='chatgpt_list'),
    # chatgpt history
    path('chatgpt_history/', views.chatgpt_history_view, name='chatgpt_history'),
    # export chatgpt history
    path('export_chatgpt_history/', views.export_chatgpt_history_view, name='export_chatgpt_history'),
    # chatgpt detail
    path('<slug>/', views.get_chatgpt_detail_view, name='get_chatgpt_detail'),
    # delete chatgpt list
    path('<slug>/delete_chatgpt_list/', views.delete_chatgpt_list_view, name='delete_chatgpt_list'),
    # delete chatgpt history
    path('<slug>/delete_chatgpt_history/', views.delete_chatgpt_history_view, name='delete_chatgpt_history'),
]
