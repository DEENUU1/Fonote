from django.db import models


class Price(models.Model):
    price = models.DecimalField(max_digits=6, decimal_places=2, null=False)
    prev_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    stripe_id = models.CharField(max_length=250, null=False)

    def __str__(self):
        return f"{self.price}"

    class Meta:
        verbose_name = "Price"
        verbose_name_plural = "Prices"
