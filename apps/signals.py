from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.models import User


@receiver(pre_save, sender=User)
def user_pre_save(sender, instance: User, **kwargs):
    if instance.pk is None:  # and (not isinstance(instance.balance, int) or instance.balance == 0):
        # instance.balance = 5000

        send_mail(
            'Tema',
            'You signed up successfully',
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
        )
