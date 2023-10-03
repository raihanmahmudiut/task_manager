
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Task
from django.http import JsonResponse
import json  # Make sure to import the json module
from django.contrib.auth.models import User

from .forms import TaskForm

@login_required
def task_list(request):
    tasks = Task.objects.all() # Fetch tasks for the logged-in user
    users = User.objects.all()  # Fetch all registered users
    return render(request, 'index.html', {'tasks': tasks, 'users': users})




def delete_task(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
        task.delete()
        return JsonResponse({"message": "Task deleted successfully"})
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)

def edit_task(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
        if request.method == "PUT":
            data = json.loads(request.body)
            new_text = data.get("text", "")
            task.text = new_text
            task.save()
            return JsonResponse({"message": "Task edited successfully"})
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)




@login_required
def create_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        due_date = request.POST['due_date']
        status = request.POST['status']
        assigned_user_id = request.POST['user']  # Get the assigned user ID from the form

        # Create a task associated with the assigned user
        task = Task.objects.create(
            user=User.objects.get(id=assigned_user_id),
            title=title,
            description=description,
            due_date=due_date,
            status=status
        )

        return redirect('task_list')  # Redirect to a task list view

    # Fetch all registered users
    users = User.objects.all()

    return render(request, 'tasks/create_task.html', {'users': users})


