from django.contrib import admin

from .models import FileUpload, VectorDBArchive, ActiveVectorDB, LLMSettings


class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'doc_location', 'doc_file', 'date_posted')
    search_fields = ('author', 'doc_file')
    readonly_fields = ('id', 'author')
    list_per_page = 25

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class VectorDBArchiveAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'vector_db', 'db_name', 'db_elements', 'date_created')
    search_fields = ('author', 'vector_db', 'db_name')
    readonly_fields = ('id', 'author')
    list_per_page = 25

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class ActiveVectorDBAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'vector_db', 'db_name')
    search_fields = ('author', 'vector_db', 'db_name')
    readonly_fields = ('id', 'author')
    list_per_page = 25

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class LLMSettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'llm', 'llm_model', 'vector_db', 'date_created')
    search_fields = ('author', 'llm', 'llm_model', 'vector_db')
    readonly_fields = ('id', 'author')
    list_per_page = 25

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(FileUpload, FileUploadAdmin)
admin.site.register(VectorDBArchive, VectorDBArchiveAdmin)
admin.site.register(ActiveVectorDB, ActiveVectorDBAdmin)
admin.site.register(LLMSettings, LLMSettingsAdmin)
