from django.urls import path

from .views import (
    input_pk_get_delete,
    input_post_get,
    result_list,
    result_create,
)

urlpatterns = [
    path("input/", input_post_get.InputAPIView.as_view(), name="input_post_list"),
    path("input/<str:pk>/", input_pk_get_delete.InputPkAPIView.as_view(), name="input_details"),
    path("result/", result_create.ResultCreateAPIView.as_view(), name="result_create"),
    path("result/<str:pk>", result_list.ResultListAPIView.as_view(), name="result_list"),

]
