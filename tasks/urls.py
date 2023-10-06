from django.urls import include, path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("task_list/", views.task_list, name="task_list"),
    path("create_task/", views.create_task, name="create_task"),
    path(
        "update_status/<int:task_id>/",
        views.update_task,
        name="update_task_status",
    ),  # Include the API-level URLs here
]

urlpatterns = format_suffix_patterns(urlpatterns)
