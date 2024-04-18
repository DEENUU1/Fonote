from django.urls import path
from .views import CreateSubscription


urlpatterns = [
    path('create/', CreateSubscription.as_view(), name='create_subscription'),
]