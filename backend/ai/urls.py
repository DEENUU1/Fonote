from django.urls import path
from .views import InputAPIView, InputPkAPIView

urlpatterns = [
    path("input/", InputAPIView.as_view(), name="input_post_list"),
    path("input/<str:pk>/", InputPkAPIView.as_view(), name="input_details"),
]