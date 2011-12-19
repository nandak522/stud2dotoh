from django.db import models
from utils.models import BaseModel, BaseModelManager
from django.template.defaultfilters import slugify
from users.models import UserProfile
from utils.session_stash import SessionStashable
from taggit.managers import TaggableManager

class TaskAlreadyExistsException(Exception):
    pass

class TaskManager(BaseModelManager):
    def create_task(self, title, creator, tags, description='', is_public=True, deadline=None):
        """
        Usage:create_task(title='<some title goes here>',
                          creator='<userprofile object>',
                          tags='comma separated string containing tags',
                          description='<text containing the description of the task>',
                          is_public=True,
                          deadline=<datetime object containing the deadline of the task>)
        """
        if not self.filter(title=title).count():
            task = Task(title=title,
                        slug=slugify(title),
                        description=description,
                        creator=creator,
                        is_public=is_public,
                        deadline=deadline)
            task.save()
            task.tags.add(*tags)
            return task
        raise TaskAlreadyExistsException

class Task(BaseModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    creator = models.ForeignKey(UserProfile)
    deadline = models.DateField(blank=True, null=True)
    is_public = models.BooleanField(default=True)
    objects = TaskManager()
    tags = TaggableManager()

    def current_assignees(self):
        return self.taskmembership_set.exclude(status='FINISHED').values('userprofile')

    def solvers(self):
        return self.taskmembership_set.filter(status='FINISHED').values('userprofile')

    def __unicode__(self):
        return self.title

    def all_solutions(self):
        return self.tasksolution_set.all()

    @models.permalink
    def get_absolute_url(self):
        return ('task', (), {'task_id':self.id, 'task_slug':self.slug})

    def solve(self, description, solved_by):
        solution = TaskSolution(task=self, description=description, created_by=solved_by)
        solution.save()

class TaskAlreadyAssignedException(Exception):
    pass

class TaskSolution(BaseModel, SessionStashable):
    session_variable = 'solutions_stash'

    created_by = models.ForeignKey(UserProfile, null=True, blank=True)
    description = models.TextField()
    task = models.ForeignKey(Task)

    def __unicode__(self):
        return "%s... ==> %s... ==> %s" % (self.task.title[:10], self.description[:10], self.created_by)

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
    status = models.CharField(choices=_status_choices, max_length=10, default='INPROGRESS')
    finished_on = models.DateField(blank=True, null=True)
    objects = TaskMembershipManager()

    def __unicode__(self):
        return '%s ==> %s' % (self.task ,self.userprofile)

class TaskLevel(BaseModel):
    level = models.CharField(max_length=50)
    task = models.OneToOneField(Task)

    #NOTE:All the interactions related to TaskLevel model happen through
    #Task model. Like task.tasklevel, TaskLevel() if the former raises a
    #DoesNotExist error

    def __unicode__(self):
        return '%s ==> %s' % (self.task.title, self.level)
