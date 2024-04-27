from django.urls import path

from .views import (
    input_pk_get_delete,
    input_post,
    result_list,
    result_create,
    input_get
)

urlpatterns = [
    path("input/all/", input_get.InputListAPIView.as_view(), name="input_list"),
    path("input/", input_post.InputCreateAPIView.as_view(), name="input_create"),
    path("input/<str:pk>/", input_pk_get_delete.InputPkAPIView.as_view(), name="input_details"),
    path("result/", result_create.ResultCreateAPIView.as_view(), name="result_create"),
    path("result/<str:pk>", result_list.ResultListAPIView.as_view(), name="result_list"),

]
