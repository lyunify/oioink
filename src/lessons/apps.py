from django.apps import AppConfig


class LessonsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lessons'
    
    def ready(self):
        """When app is ready, import signal handlers"""
        import lessons.signals