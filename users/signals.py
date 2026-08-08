from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a profile automatically after a new user is created.

    Args:
        sender: The model class that sent the signal.
        instance: The newly created User instance.
        created: True if a new User was created, otherwise False.
        **kwargs: Additional arguments provided by the Django signal.

    This signal ensures that every newly registered user
    automatically receives an associated Profile instance.
    """
    if created:
        Profile.objects.create(
            user=instance
        )