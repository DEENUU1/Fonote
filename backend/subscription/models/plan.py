from django.db import models
from .price import Price


class Plan(models.Model):
    name = models.CharField(max_length=20, null=False)
    description = models.TextField(null=True)
    youtube = models.BooleanField(default=True)
    spotify = models.BooleanField(default=False)
    max_result = models.IntegerField(null=False, default=60)
    max_input = models.IntegerField(null=False, default=15)
    duration = models.IntegerField(null=False)
    price = models.ForeignKey(Price, on_delete=models.CASCADE)
    change_lang = models.BooleanField(default=False)
    ai_transcription = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Plans"

