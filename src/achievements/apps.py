from django.apps import AppConfig


class AchievementsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'achievements'
    
    def ready(self):
        """When app is ready, import signal handlers"""
        import achievements.signals

