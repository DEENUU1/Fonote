from django.urls import path
from .views import (
    cancel_subscription,
    create_checkout,
    get_invoice,
    order_details,
    order_list,
    plan_list,
    stripe_webhook,
    user_subscription
)


urlpatterns = [
    path("plan/", plan_list.PlanListAPIView.as_view(), name="plan_list"),
    path("order/", order_list.OrderListAPIView.as_view(), name="order_list"),
    path("order/<str:pk>/", order_details.OrderDetailsAPIView.as_view(), name="order_details"),
    path("invoice/<str:pk>/", get_invoice.GetInvoice.as_view(), name="get_invoice"),
    path('checkout/', create_checkout.CreateSubscription.as_view(), name='create_subscription'),
    path('cancel/', cancel_subscription.CancelSubscription.as_view(), name='cancel_subscription'),
    path('webhook/', stripe_webhook.Webhook.as_view()),
    path('subscription/', user_subscription.UserSubscriptionAPIView.as_view(), name="user_current_subscription")
]