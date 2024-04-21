from django.urls import path
from .views.create_contact import ContactCreateAPIView


urlpatterns = [
    path("/", ContactCreateAPIView.as_view(), name="create_contact"),
]
