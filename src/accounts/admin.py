from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account, Profile


class AccountAdmin(UserAdmin):
    list_display = ('id', 'email', 'username', 'signup_date',
                    'last_signin', 'is_staff', 'is_admin', 'is_email_verified')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    readonly_fields = ('id', 'email', 'signup_date', 'last_signin')
    list_per_page = 25

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name')
    search_fields = ('user', 'first_name', 'last_name')
    readonly_fields = ('id', 'user', )
    list_per_page = 25

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)
admin.site.register(Profile, ProfileAdmin)
