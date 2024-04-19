from django.contrib import admin
from .models import plan, price, user_subscription, order


class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "active")
    list_filter = ("active",)


class PriceAdmin(admin.ModelAdmin):
    list_display = ("price", "prev_price")


class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "total_amount", "invoice_url")


class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "start_date", "end_date", "status", "order")
    list_filter = ("status", "plan")


admin.site.register(plan.Plan, PlanAdmin)
admin.site.register(price.Price, PriceAdmin)
admin.site.register(user_subscription.UserSubscription, UserSubscriptionAdmin)
admin.site.register(order.Order, OrderAdmin)
