from django import forms
from .models import Task
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    assigned_user = forms.ModelChoiceField(queryset=User.objects.all(), label='Assign To', required=False)

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'status', 'assigned_user']
