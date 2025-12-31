from django.contrib import admin

from .models import ChatGPTDB


class ChatGPTDBAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'user_message', 'ai_message', 'date_posted')
    search_fields = ('author', 'user_message')
    readonly_fields = ('id', 'date_posted')
    list_per_page = 25

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(ChatGPTDB, ChatGPTDBAdmin)
