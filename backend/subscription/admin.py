from django.contrib import admin
from .models import plan, order, price, user_subscription


class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "active")
    list_filter = ("active",)


class PriceAdmin(admin.ModelAdmin):
    list_display = ("price", "prev_price")


admin.site.register(plan.Plan, PlanAdmin)
admin.site.register(price.Price, PriceAdmin)
