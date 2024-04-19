from django.urls import path
from .views import (
    CreateSubscription,
    WebHook,
    PlanListAPIView,
    OrderListAPIView,
    OrderDetailsAPIView,
    CancelSubscription,
    GetInvoice
)


urlpatterns = [
    path("plan/", PlanListAPIView.as_view(), name="plan_list"),
    path("order/", OrderListAPIView.as_view(), name="order_list"),
    path("order/<str:pk>/", OrderDetailsAPIView.as_view(), name="order_details"),
    path("invoice/<str:pk>/", GetInvoice.as_view(), name="get_invoice"),
    path('checkout/', CreateSubscription.as_view(), name='create_subscription'),
    path('cancel/', CancelSubscription.as_view(), name='cancel_subscription'),
    path('webhook/', WebHook.as_view()),
]