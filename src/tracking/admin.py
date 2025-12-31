from django.contrib import admin
from .models import Spending, SpendingCategory, Saving, SavingGoal


class SpendingAdmin(admin.ModelAdmin):
    list_display = ('date', 'amount', 'description', 'child_name', 'category', 'user', 'created_at')
    list_filter = ('date', 'category', 'child_name', 'created_at')
    search_fields = ('description', 'child_name', 'user__username')
    date_hierarchy = 'date'
    ordering = ('-date', '-created_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'date', 'amount', 'description', 'child_name')
        }),
        ('Category', {
            'fields': ('category',)
        }),
    )


class SpendingCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'color')
    search_fields = ('name',)


class SavingAdmin(admin.ModelAdmin):
    list_display = ('date', 'amount', 'description', 'child_name', 'goal', 'user', 'created_at')
    list_filter = ('date', 'child_name', 'created_at')
    search_fields = ('description', 'child_name', 'goal', 'user__username')
    date_hierarchy = 'date'
    ordering = ('-date', '-created_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'date', 'amount', 'description', 'child_name')
        }),
        ('Goal', {
            'fields': ('goal',)
        }),
    )


class SavingGoalAdmin(admin.ModelAdmin):
    list_display = ('goal_name', 'target_amount', 'current_amount', 'progress_percentage', 'child_name', 'user', 'is_completed', 'created_at')
    list_filter = ('created_at', 'child_name', 'deadline')
    search_fields = ('goal_name', 'description', 'child_name', 'user__username')
    readonly_fields = ('current_amount', 'progress_percentage', 'remaining_amount', 'is_completed', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'goal_name', 'target_amount', 'child_name', 'description')
        }),
        ('Visual Settings', {
            'fields': ('icon', 'color')
        }),
        ('Deadline', {
            'fields': ('deadline',)
        }),
        ('Progress (Read-only)', {
            'fields': ('current_amount', 'remaining_amount', 'progress_percentage', 'is_completed')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


admin.site.register(Spending, SpendingAdmin)
admin.site.register(SpendingCategory, SpendingCategoryAdmin)
admin.site.register(Saving, SavingAdmin)
admin.site.register(SavingGoal, SavingGoalAdmin)


