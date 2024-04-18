import uuid
from django.db import models
from utils.base_model import BaseModel
from django.contrib.auth.backends import UserModel
from .plan import Plan


class UserSubscription(BaseModel):
    STATUS = (
        ("ACTIVE", "ACTIVE"),
        ("CANCELED", "CANCELED"),
        ("EXPIRED", "EXPIRED"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(UserModel, on_delete=models.SET_NULL, null=True)
    subscription_id = models.CharField(max_length=255, unique=True)
    plan = models.OneToOneField(Plan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    status = models.CharField(max_length=25, choices=STATUS, default="ACTIVE")
