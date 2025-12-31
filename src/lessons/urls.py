from django.urls import path
from . import views


app_name = 'lessons'

urlpatterns = [
    # Lesson views
    path('', views.lesson_list_view, name='lesson_list'),
    path('lesson1/', views.lesson1_view, name='lesson1'),
    path('lesson2/', views.lesson2_view, name='lesson2'),
    path('lesson3/', views.lesson3_view, name='lesson3'),
    path('lesson4/', views.lesson4_view, name='lesson4'),
    path('lesson5/', views.lesson5_view, name='lesson5'),
    path('lesson6/', views.lesson6_view, name='lesson6'),
    path('lesson7/', views.lesson7_view, name='lesson7'),
    path('lesson8/', views.lesson8_view, name='lesson8'),
    path('lesson9/', views.lesson9_view, name='lesson9'),
    path('lesson10/', views.lesson10_view, name='lesson10'),
    path('<slug:slug>/', views.lesson_detail_view, name='lesson_detail'),
    path('<slug:slug>/complete/', views.lesson_complete_view, name='lesson_complete'),
]
