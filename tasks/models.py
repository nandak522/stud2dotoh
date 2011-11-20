from django.db import models
from utils.models import BaseModel, BaseModelManager
from django.template.defaultfilters import slugify
from users.models import UserProfile

class TaskAlreadyExistsException(Exception):
    pass

class TaskManager(BaseModelManager):
    def create_task(self, title, creator, description='', is_public=True, deadline=None):
        if not self.filter(title=title).count():
            task = Task(title=title,
                        slug=slugify(title),
                        description=description,
                        creator=creator,
                        is_public=is_public,
                        deadline=deadline)
            task.save()
            return task
        raise TaskAlreadyExistsException

class Task(BaseModel):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=80, db_index=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    creator = models.OneToOneField(UserProfile)
    deadline = models.DateField(blank=True, null=True)
    is_public = models.BooleanField(default=True)
    objects = TaskManager()

    def current_assignees(self):
        return self.taskmembership_set.exclude(status='FINISHED').values('userprofile')

    def solvers(self):
        return self.taskmembership_set.filter(status='FINISHED').values('userprofile')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('task', (), {'task_id':self.id, 'task_slug':self.slug})

    @property
    def bounty(self):
        return self.taskbounty.bounty

class TaskAlreadyAssignedException(Exception):
    pass

class TaskMembershipManager(BaseModelManager):
    def assign_task(self, task, user):
        if not self.filter(task=task, user=user).count():
            taskmembership = TaskMembership(task=task,
                                  user=user)
            taskmembership.save()
            return taskmembership
        raise TaskAlreadyAssignedException

    def finish_task(self, task, user):
        self.status = 'FINISHED'
        self.userprofile.award_score(task.bounty)

class TaskMembership(BaseModel):
    _status_choices = (('INPROGRESS','In-Progress'),
                       ('FINISHED','Finished'),
    )

    task = models.ForeignKey(Task)
    userprofile = models.ForeignKey(UserProfile, related_name='assigned_tasks')
    status = models.CharField(choices=_status_choices, max_length=10)
    finished_on = models.DateField(blank=True, null=True)
    objects = TaskMembershipManager()

    def __unicode__(self):
        return '%s ==> %s' % (self.task ,self.userprofile)
        
class TaskBounty(BaseModel):
    task = models.OneToOneField(Task)
    bounty = models.IntegerField()

    def __unicode__(self):
        return '%s ==> %s' % (self.task.title, self.bounty)
