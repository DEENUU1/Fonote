from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('api/auth/', include('authentication.urls')),
    path('api/subscription/', include('subscription.urls')),
    path('api/contact', include('contact.urls')),
    path('api/ai/', include('ai.urls')),
    path("admin/", admin.site.urls),
]