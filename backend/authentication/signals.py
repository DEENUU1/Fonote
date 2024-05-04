from django.contrib.auth.backends import UserModel
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=UserModel)
def set_username_from_email(sender, instance, **kwargs):
    if not instance.pk:
        instance.username = instance.email


pre_save.connect(set_username_from_email, sender=UserModel)
