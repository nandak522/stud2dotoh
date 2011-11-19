from utils import response
from tasks.models import Task, TaskMembership
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

def view_homepage(request, homepage_template):
    return response(request, homepage_template, {'active_tab':'home'})

def view_all_tasks(request, all_tasks_template):
    tasks = Task.objects.values('id', 'slug', 'title')
    return response(request, all_tasks_template, {'tasks':tasks, 'active_tab':'alltasks'})

@login_required
def view_my_tasks(request, my_tasks_template):
    user = request.user
    tasks = TaskMembership.objects.filter(user=user).values('task__id', 'task__slug', 'task__title')
    return response(request, my_tasks_template, {'tasks':tasks, 'active_tab':'mytasks'})
    
def view_task(request, task_id, task_slug, task_template):
    task = get_object_or_404(Task, pk=task_id, slug=task_slug)
    return response(request, task_template, {'task':task})
