from django.contrib import admin
from .models import Achievement, UserAchievement


class AchievementAdmin(admin.ModelAdmin):
    list_display = ('icon', 'name', 'achievement_type', 'coin_reward', 'order', 'is_active', 'created_at')
    list_filter = ('achievement_type', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('order', 'created_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'icon', 'color', 'achievement_type')
        }),
        ('Reward', {
            'fields': ('coin_reward',)
        }),
        ('Requirements', {
            'fields': ('requirements',),
            'description': 'JSON field for storing unlock conditions. Format: {"key": "value"}'
        }),
        ('Display', {
            'fields': ('order', 'is_active')
        }),
    )


class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement', 'unlocked_at', 'is_notified')
    list_filter = ('unlocked_at', 'is_notified', 'achievement__achievement_type')
    search_fields = ('user__username', 'achievement__name')
    ordering = ('-unlocked_at',)
    readonly_fields = ('unlocked_at',)


admin.site.register(Achievement, AchievementAdmin)
admin.site.register(UserAchievement, UserAchievementAdmin)




