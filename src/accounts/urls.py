from django.urls import path
from django.contrib.auth import views
from . import views


app_name = 'accounts'

urlpatterns = [
    # account
    # path('<user_id>/', views.account_view, name='account'),
    path('account/', views.account_view, name='account'),
    path('profile/', views.profile_view, name='profile'),
    path('profile_image_update/', views.profile_image_update_view, name='profile_image_update'),
    path('settings/', views.settings_view, name='settings'),
    path('signin/', views.signin_view, name='signin'),
    path('signout/', views.signout_view, name='signout'),
    path('signup/', views.signup_view, name='signup'),
    path('validate_username/', views.validate_username, name='validate_username'),
    path('signup_verify/', views.signup_verify_view,
         name='signup_verify'),
    path(r'activate/<uidb64>[0-9A-Za-z_\-]+/<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20}',
         views.activate_view, name='activate'),
    path('must_authenticate/', views.must_authenticate_view,
         name='must_authenticate'),
]
