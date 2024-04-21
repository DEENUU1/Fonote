from django.urls import path
from .views import InputAPIView, InputPkAPIView, ResultCreateAPIView, ResultListAPIView

urlpatterns = [
    path("input/", InputAPIView.as_view(), name="input_post_list"),
    path("input/<str:pk>/", InputPkAPIView.as_view(), name="input_details"),
    path("result/", ResultCreateAPIView.as_view(), name="result_create"),
    path("result/<str:pk>", ResultListAPIView.as_view(), name="result_list"),

]