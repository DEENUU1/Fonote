from django.db import models


class Fragment(models.Model):
    start_time = models.FloatField(null=True, blank=True)
    end_time = models.FloatField(null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    text = models.TextField()
    input_data = models.ForeignKey("InputData", on_delete=models.CASCADE, related_name="fragments")

    def __str__(self):
        return f"{self.text[:50]}"

    class Meta:
        verbose_name = "Fragment"
        verbose_name_plural = "Fragments"
