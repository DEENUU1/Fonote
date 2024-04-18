from django.urls import path
from .views import CreateSubscription, WebHook


urlpatterns = [
    path('create/', CreateSubscription.as_view(), name='create_subscription'),
    path('webhook-test/', WebHook.as_view()),
]