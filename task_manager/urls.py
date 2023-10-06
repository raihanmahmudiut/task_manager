from django.contrib import admin
from django.urls import path, include  # Import the include function
from . import views  # Replace 'project_level' with your project name
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.homepage, name="homepage"),  # Homepage URL
    path("tasks/", include("tasks.urls")),  # Include task-related URLs
    path(
        "accounts/", include("authentication.urls")
    ),  # Include authentication-related URLs
    # Add other project-level URL patterns here.
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
