from datetime import timedelta

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from .models.user_subscription import UserSubscription


@receiver(pre_save, sender=UserSubscription)
def add_start_end_dates_to_user_subscription(sender, instance, **kwargs):
    """
    Adds start and end dates to a UserSubscription instance before saving if it's status is "ACTIVE" and
    start_date is not already set.

    Parameters:
    - sender: The model class of the sender.
    - instance: The UserSubscription instance being saved.
    - kwargs: Additional keyword arguments.

    Returns:
    - None
    """
    if instance.status == "ACTIVE" and not instance.start_date:
        instance.start_date = timezone.now().date()

        plan_duration = instance.plan.duration
        instance.end_date = instance.start_date + timedelta(days=plan_duration)


pre_save.connect(add_start_end_dates_to_user_subscription, sender=UserSubscription)
