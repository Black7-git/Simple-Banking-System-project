from django.apps import AppConfig


class PetsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pets"
    verbose_name = "Pets"

    def ready(self) -> None:  # pragma: no cover
        # Import signal handlers
        from . import signals  # noqa: F401
        return super().ready()
