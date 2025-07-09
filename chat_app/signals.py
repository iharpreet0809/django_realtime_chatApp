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
        instance.profile.save()
    except Profile.DoesNotExist:
        # This can happen during initial user creation if the signal fires
        # before the profile is created. The create_user_profile signal
        # will handle the creation.
        Profile.objects.create(user=instance)