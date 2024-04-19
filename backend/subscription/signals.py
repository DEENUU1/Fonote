from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models.user_subscription import UserSubscription
from django.utils import timezone


@receiver(post_save, sender=UserSubscription)
def add_start_end_dates_to_user_subscription(sender, instance, created, **kwargs):
    if instance.status == "ACTIVE":
        instance.start_date = timezone.now().date()

        plan_duration = instance.plan.duration
        instance.end_date = instance.start_date + timedelta(days=plan_duration)

        instance.save()


post_save.connect(add_start_end_dates_to_user_subscription, sender=UserSubscription)
