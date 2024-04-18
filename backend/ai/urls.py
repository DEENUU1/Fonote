from django.urls import path
from .views import InputAPIView


urlpatterns = [
    path("input/", InputAPIView.as_view(), name="input_post"),
]