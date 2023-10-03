from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create/', views.create_task, name='create_task'),  # New task creation view
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('edit-task/<int:task_id>/', views.edit_task, name='edit_task'),  # Main task list view
]