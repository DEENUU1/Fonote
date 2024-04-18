from django.urls import path
from .views import CreateSubscription, WebHook, PlanListAPIView


urlpatterns = [
    path("plan/", PlanListAPIView.as_view(), name="plan_list"),

    path('create/', CreateSubscription.as_view(), name='create_subscription'),
    path('webhook-test/', WebHook.as_view()),
]