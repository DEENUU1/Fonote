from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
app = Celery("core")
app.config_from_object(settings, namespace="CELERY")
app.autodiscover_tasks()


app.conf.beat_schedule = {
    # Task to change status of expired subscription
    # Run every 24H
    "mark_expired_user_subscriptions_as_expired": {
        "task": "subscription.tasks.mark_expired_user_subscriptions_as_expired",
        "schedule": 86400,
    },
}
