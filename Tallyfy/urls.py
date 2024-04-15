from django.contrib import admin
from django.urls import include, path
from operations import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(("operations.urls", "operations"), namespace="operations")),
]
