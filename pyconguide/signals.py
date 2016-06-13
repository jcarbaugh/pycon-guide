from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from pyconguide.models import Calendar


@receiver(post_save, sender=User, dispatch_uid="pcg_create_user_calendar")
def create_user_calendar(sender, instance, created, **kwargs):
    if created:
        Calendar.objects.create(user=instance)
