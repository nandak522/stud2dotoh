from django.conf.urls.defaults import patterns

urlpatterns = patterns('tasks.views',
    (r'^$', 'view_all_tasks', {'all_tasks_template':'all_tasks.html'}, 'all_tasks'),
    (r'^my/$', 'view_my_tasks', {'my_tasks_template':'my_tasks.html'}, 'my_tasks'),
    (r'^(?P<task_id>\d+)/(?P<task_slug>[\w\s-]+)/$', 'view_task', {'task_template':'task.html'}, 'task'),
    (r'^(?P<task_id>\d+)/submitsol/$', 'view_submit_solution', {'task_template':'task.html'}, 'submit_solution'), 
)
