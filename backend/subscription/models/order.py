import uuid
from django.db import models

from subscription.models import Plan
from utils.base_model import BaseModel
from django.contrib.auth.backends import UserModel


class Order(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    currency = models.CharField(max_length=10, null=True, blank=True)
    customer = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=10, null=True, blank=True)
    line1 = models.CharField(max_length=250, null=True, blank=True)
    line2 = models.CharField(max_length=250, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=250, null=True, blank=True)
    total_amount = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    invoice_id = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.invoice_id

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"
