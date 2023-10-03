from django import forms
from django.contrib import admin
from .models import Task

class TaskAdminForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

class TaskAdmin(admin.ModelAdmin):
    form = TaskAdminForm
    list_display = ('title', 'description', 'due_date', 'status', 'user')

    def has_add_permission(self, request):
        return True  # Allow the "Add" action

    def has_change_permission(self, request, obj=None):
        return True  # Allow the "Change" action

    def has_delete_permission(self, request, obj=None):
        return True  # Allow the "Delete" action

# Register the Task model with the custom admin class
admin.site.register(Task, TaskAdmin)
