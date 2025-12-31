from django.contrib import admin
from .models import Prize


@admin.register(Prize)
class PrizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'category', 'coin_cost', 'stock_quantity', 'status', 'is_featured', 'priority', 'created_at')
    list_filter = ('category', 'status', 'is_featured', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'icon', 'image')
        }),
        ('Category and Status', {
            'fields': ('category', 'status', 'is_featured', 'priority')
        }),
        ('Pricing and Stock', {
            'fields': ('coin_cost', 'stock_quantity', 'available_from', 'available_until')
        }),
        ('Age Restrictions', {
            'fields': ('min_age', 'max_age'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()




