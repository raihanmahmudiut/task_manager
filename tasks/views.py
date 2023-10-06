from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Task
from django.http import JsonResponse
import json  # Make sure to import the json module
from django.contrib.auth.models import User

from .forms import TaskForm


def task_list(request):
    tasks = Task.objects.all()  # Fetch tasks for the logged-in user
    users = User.objects.all()  # Fetch all registered users
    return render(request, "index.html", {"tasks": tasks, "users": users})


@login_required
def create_task(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        due_date = request.POST["due_date"]
        status = request.POST["status"]
        assigned_user_id = request.POST[
            "user"
        ]  # Get the assigned user ID from the form

        # Create a task associated with the assigned user
        task = Task.objects.create(
            user=User.objects.get(id=assigned_user_id),
            title=title,
            description=description,
            due_date=due_date,
            status=status,
        )

        return redirect("task_list")  # Redirect to a task list view

    # Fetch all registered users
    users = User.objects.all()

    return render(request, "tasks/create_task.html", {"users": users})


@login_required
def update_task(request, task_id):
    if request.method == "POST":
        try:
            task = Task.objects.get(id=task_id)  # Corrected 'objects' typo
            # Initiating new status
            new_status = request.POST.get("status")

            # Updating the status
            task.status = new_status
            task.save()

            return redirect("task_list")
        except Task.DoesNotExist:
            return JsonResponse({"message": "Task not found"}, status=404)
    return JsonResponse({"message": "Invalid Request"})
