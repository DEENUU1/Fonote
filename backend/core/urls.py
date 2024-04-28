from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Fonote",
      default_version='v1',
      description="Docs...",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/auth/', include('authentication.urls')),
    path('api/subscription/', include('subscription.urls')),
    path('api/contact', include('contact.urls')),
    path('api/ai/', include('ai.urls')),
    path("admin/", admin.site.urls),
]