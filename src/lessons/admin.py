from django.contrib import admin

from .models import Lesson, LessonSection, LessonTip, UserLessonProgress


class LessonSectionInline(admin.TabularInline):
    model = LessonSection
    extra = 1
    fields = ('title', 'section_type', 'order', 'icon')
    ordering = ('order',)


class LessonTipInline(admin.TabularInline):
    model = LessonTip
    extra = 1
    fields = ('title', 'icon', 'order')
    ordering = ('order',)


class LessonAdmin(admin.ModelAdmin):
    list_display = ('lesson_number', 'title', 'status', 'age_range', 'coin_reward', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [LessonSectionInline, LessonTipInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('lesson_number', 'title', 'slug', 'subtitle', 'description')
        }),
        ('Visual Elements', {
            'fields': ('cover_image', 'icon')
        }),
        ('Lesson Information', {
            'fields': ('age_range', 'duration_minutes', 'coin_reward', 'status')
        }),
    )


class UserLessonProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'status', 'started_at', 'completed_at', 'created_at')
    list_filter = ('status', 'created_at', 'completed_at')
    search_fields = ('user__username', 'lesson__title')
    ordering = ('-updated_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'lesson', 'status')
        }),
        ('Timestamps', {
            'fields': ('started_at', 'completed_at', 'created_at', 'updated_at')
        }),
    )


admin.site.register(Lesson, LessonAdmin)
admin.site.register(LessonSection)
admin.site.register(LessonTip)
admin.site.register(UserLessonProgress, UserLessonProgressAdmin)
