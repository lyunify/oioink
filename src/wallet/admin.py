from django.contrib import admin
from .models import Wallet, WalletTransaction


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'child_name', 'coin_name', 'is_practice_mode', 'balance', 'created_at']
    list_filter = ['is_practice_mode', 'user', 'child_name', 'created_at']
    search_fields = ['user__username', 'child_name', 'coin_name']
    readonly_fields = ['balance', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'child_name', 'coin_name', 'coin_icon')
        }),
        ('Practice Mode', {
            'fields': ('is_practice_mode', 'practice_initial_balance'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('balance',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ['wallet', 'transaction_type', 'amount', 'description', 'date', 'created_at']
    list_filter = ['transaction_type', 'date', 'created_at']
    search_fields = ['wallet__child_name', 'description']
    readonly_fields = ['created_at', 'updated_at']

