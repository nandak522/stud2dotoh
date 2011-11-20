from django.contrib import admin
from tasks.models import Task, TaskBounty, TaskMembership

class TaskAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}
    list_per_page = 25
    list_display = ('title', 'deadline', 'creator', 'is_public')
    search_fields = ('title', 'deadline')
    
class TaskBountyAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_display = ('task', 'bounty')
    search_fields = ('task',)
    verbose_name_plural = 'TaskBounties'

class TaskMembershipAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_display = ('task', 'userprofile')
    search_fields = ('task', 'userprofile')
    verbose_name_plural = 'TaskMemberships'
    
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskBounty, TaskBountyAdmin)
admin.site.register(TaskMembership, TaskMembershipAdmin)
