from django.urls import include, path
from . import views

urlpatterns = [
    path("api/", include("tasks.api.urls")),
    path("tasks/<int:task_id>", views.task_detail),
]
