from django.urls import path
from . import views


app_name = 'myhome'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('terms/', views.terms_view, name='terms'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('news/', views.news_view, name='news'),
    path('about_miracles/', views.about_miracles_view, name='about_miracles'),
    path('faqs/', views.faqs_view, name='faqs'),
    path('support/', views.support_view, name='support'),
    path('complete-onboarding/', views.complete_onboarding_view, name='complete_onboarding'),
]
