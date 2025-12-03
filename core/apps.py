from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'Core app for CampusFind'

    def ready(self):
        # import signal handlers
        from . import signals  # noqa: F401
