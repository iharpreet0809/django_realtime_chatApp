# Create this new file to handle signals if you add more complex logic,
# for now it's just for connecting the profile creation.

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        # Only save if profile exists, don't create a new one
        # This prevents overwriting profile data set elsewhere
        if hasattr(instance, 'profile'):
            # Don't call save() here as it might overwrite data
            pass
    except Profile.DoesNotExist:
        # Only create if no profile exists
        Profile.objects.create(user=instance)