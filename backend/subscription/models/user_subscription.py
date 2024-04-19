import uuid
from django.db import models
from utils.base_model import BaseModel
from django.contrib.auth.backends import UserModel
from .plan import Plan
from .order import Order


class UserSubscription(BaseModel):
    STATUS = (
        ("PENDING", "PENDING"),
        ("ACTIVE", "ACTIVE"),
        ("CANCELED", "CANCELED"),
        ("FAILED", "FAILED"),
        ("PAID", "PAID"),
        ("EXPIRED", "EXPIRED"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    subscription_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=25, choices=STATUS, default="PENDING")
    session_id = models.CharField(max_length=255, null=False, blank=False)
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.user}-{self.status}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "UserSubscription"
        verbose_name_plural = "UserSubscriptions"
