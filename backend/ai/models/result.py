import uuid
from django.db import models
from utils.base_model import BaseModel
from .input_data import InputData


class Result(BaseModel):
    RESULT = (
        ("SUMMARY", "SUMMARY"),
        ("NOTE", "NOTE"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(null=True, blank=True)
    result_type = models.CharField(max_length=25, choices=RESULT, null=False)
    input = models.ForeignKey(InputData, on_delete=models.CASCADE, related_name='results')

    def __str__(self):
        return f"{self.id}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Result"
        verbose_name_plural = "Results"
