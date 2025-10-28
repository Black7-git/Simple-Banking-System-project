from django.apps import AppConfig


class PetsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pets'

    def ready(self) -> None:
        # Import signals
        try:
            from . import signals  # noqa: F401
        except Exception:
            # Avoid errors during initial migration when tables don't exist
            pass
