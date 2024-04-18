from utils.base_model import BaseModel
from django.db import models
from django.contrib.auth.backends import UserModel
from .plan import Plan


class Order(BaseModel):
    STATUS = (
        ("PENDING", "PENDING"),
        ("COMPLETED", "COMPLETED"),
        ("CANCELLED", "CANCELLED"),
    )
    user = models.OneToOneField(UserModel, on_delete=models.SET_NULL, null=True)
    plan = models.OneToOneField(Plan, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=25, choices=STATUS, default="PENDING")
