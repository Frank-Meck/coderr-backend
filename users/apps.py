from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Configuration for the users application.

    Defines the application name and ensures that the users'
    Django signals are registered when the application is ready.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        """
        Import the users signals when the application is ready.

        This ensures that the post-save signal for automatically
        creating user profiles is registered with Django.
        """
        import users.signals
