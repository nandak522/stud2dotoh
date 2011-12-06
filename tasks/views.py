from utils import response
from tasks.models import Task, TaskMembership, TaskSolution
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

def view_homepage(request, homepage_template):
    return response(request, homepage_template, {'active_tab':'home'})

def view_all_tasks(request, all_tasks_template):
    tasks = Task.objects.values('id', 'slug', 'title')
    return response(request, all_tasks_template, {'tasks':tasks,
                                                  'active_tab':'alltasks'})

@login_required
def view_my_tasks(request, my_tasks_template):
    user = request.user
    tasks = TaskMembership.objects.filter(user=user).values('task__id',
                                                            'task__slug',
                                                            'task__title')
    return response(request, my_tasks_template, {'tasks':tasks,
                                                 'active_tab':'mytasks'})
    
def view_task(request, task_id, task_slug, task_template):
    task = get_object_or_404(Task, pk=task_id, slug=task_slug)
    #TODO:all_solutions is supposed to have Both Anonymous and Authenticated Solutions
    all_solutions = task.all_solutions() 
    #all_stashes = TaskSolution.get_stashed_in_session(request.session)
    return response(request, task_template, {'task':task,
                                             'all_solutions':all_solutions})

def view_submit_solution(request, task_id, task_template):
    task = get_object_or_404(Task, pk=task_id)
    
    return response(request, task_template, {'tasks':task})
