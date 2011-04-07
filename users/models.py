from datetime import timedelta
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import connection
from django.db import models
from utils import slugify
from utils.models import BaseModel, BaseModelManager, YearField
import hashlib
import os

branches = (('CSE', 'Computers'),
            ('ME', 'Mechanical'),
            ('CVE', 'Civil'),
            ('ECE', 'Electronics & Communications'),
            ('EEE', 'Electrical & Electronics'),
            ('IE', 'Instrumentation'),
            ('CHE', 'Chemical'),
            ('TXE', 'Textile'),
            ('BTE', 'Bio-Tech'),
            ('MNE', 'Mining'),
            ('ENVE', 'Environmental'),
            ('PYE', 'Polymer'),
            ('BME', 'Bio-Medical'),
            ('CCE', 'Ceramics & Cement'),
            ('PTE', 'Printing'),
            )

SLUG_UPDATE_TIME_THRESHOLD_IN_SECONDS = 2

class UserProfileAlreadyExistsException(Exception):
    pass

class CantUpdateSlugAgainException(Exception):
    pass

class UserProfileManager(BaseModelManager):
    def create_profile(self, email, password, name):
        if self.exists(user__email=email):
            raise UserProfileAlreadyExistsException
        user = User.objects.create_user(username=self._compute_username(email),
                                        email=email,
                                        password=password)
        userprofile = UserProfile(user=user, name=name, slug=slugify(name))
        userprofile.save()
        return userprofile
    
    def _compute_username(self, email):
        return hashlib.sha1(email).hexdigest()[:30]
    
class UserProfile(BaseModel):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(max_length=50, db_index=True)#this will be used as his unique url identifier
    objects = UserProfileManager()
    
    def __unicode__(self):
        return self.name

    @property
    def asked_questions(self):
        return self.question_set.values('title', 'id', 'slug')
    
    @property
    def answered_questions(self):
        from quest.models import Question
        #FIXME:the above import globally is causing circular import error
        answers_ids = tuple([question['question_id'] for question in self.answer_set.values('question_id')])
        return Question.objects.filter(id__in=answers_ids).values('title', 'id', 'slug')
    
    @property
    def group_name(self):
        user_groups = self.user.groups
        if user_groups.count():
            return self.user.groups.all()[0].name
        return ''
    
    def make_student(self):
        user_groups = self.user.groups
        for group in user_groups.all():
            user_groups.remove(group)
        user_groups.add(Group.objects.get(name='Student'))
        
    def make_employee(self):
        user_groups = self.user.groups
        for group in user_groups.all():
            user_groups.remove(group)
        user_groups.add(Group.objects.get(name='Employee'))
        
    def make_professor(self):
        user_groups = self.user.groups
        for group in user_groups.all():
            user_groups.remove(group)
        user_groups.add(Group.objects.get(name='Professor'))
    
    @property    
    def is_student(self):
        return Group.objects.get(name="Student") in self.user.groups.all() 
        
    @property
    def is_professor(self):
        return Group.objects.get(name="Professor") in self.user.groups.all()
        
    @property
    def is_employee(self):
        return Group.objects.get(name="Employee") in self.user.groups.all()
    
    def join_college(self, college_name, branch='', start_year=None, end_year=None, aggregate=None):
        AcadInfo.objects.filter(userprofile=self).delete()
        college_slug = slugify(college_name)
        if College.objects.exists(slug=college_slug):
            college = College.objects.get(slug=college_slug)
        else:
            college = College.objects.create_college(name=college_name)
        AcadInfo.objects.create_acadinfo(self, branch=branch, college=college, start_year=start_year, end_year=end_year, aggregate=aggregate)
        
    def join_workplace(self, workplace_name, workplace_type, designation='', years_of_exp=''):
        workplace_slug = slugify(workplace_name)
        if workplace_type and (self.is_employee or self.is_professor):
            if workplace_type == 'Company':
                if Company.objects.exists(slug=workplace_slug):
                    workplace = Company.objects.get(slug=workplace_slug)
                else:
                    workplace = Company.objects.create_company(name=workplace_name)
            elif workplace_type == 'College':
                if College.objects.exists(slug=workplace_slug):
                    workplace = College.objects.get(slug=workplace_slug)
                else:
                    workplace = College.objects.create_college(name=workplace_name)
            WorkInfo.objects.filter(userprofile=self).delete()
            WorkInfo.objects.create_workinfo(self, workplace=workplace, designation=designation, years_of_exp=years_of_exp)
        else:
            raise Exception, 'Student cant join a Workplace. He needs to be an Employee'
        
    @property
    def acad_details(self):
        acad_details = self.acadinfo_set
        if acad_details.count():
            acad_details = acad_details.values('branch', 'college', 'start_year', 'end_year', 'aggregate')[0]
            return (acad_details['branch'], College.objects.get(id=acad_details['college']), acad_details['start_year'], acad_details['end_year'], acad_details['aggregate'])
        return ('', None, '', '', '')
        
    @property
    def work_details(self):
        work_details = self.workinfo_set
        if work_details.count():
            work_details = work_details.values('content_type', 'object_id', 'designation', 'years_of_exp')[0]
            content_type = ContentType.objects.get(id=work_details['content_type'])
            return (content_type.get_object_for_this_type(id=work_details['object_id']), work_details['designation'], work_details['years_of_exp'] if work_details['years_of_exp'] else '')
        return (None, '', '')
    
    @property
    def interested_tags(self):
        #NOTE:For now, all Q&A tags related to this user are pulled up. 
        all_qa_tags = []
        all_raised_questions = self.question_set.all()
        for question in all_raised_questions:
            all_qa_tags.extend([tag['name'] for tag in question.tags.values('name')])
        all_given_answers = self.answer_set.all()
        for answer in all_given_answers:
            question_tags = [tag['name'] for tag in answer.question.tags.values('name')]
            all_qa_tags.extend(question_tags)
        return tuple(set(all_qa_tags))
    
    @property
    def helped_persons(self):
        persons = []
        all_given_answers = self.answer_set.all()
        for answer in all_given_answers:
            person = answer.question.raised_by
            if person.id != self.id:
                persons.append((person.id, person.slug, person.name))
        return persons
        
    def update(self, **kwargs):
        if 'password' in kwargs.keys():
            self.update_password(kwargs['password'])
            kwargs.pop('password')
        if 'slug' in kwargs.keys() and self.can_update_slug():
            self.update_slug(kwargs['slug'])
            kwargs.pop('slug')
        for key in kwargs:
            setattr(self, key, kwargs[key])
        self.save()
    
    def can_update_slug(self):
        if self.modified_on <= (self.created_on + timedelta(seconds=SLUG_UPDATE_TIME_THRESHOLD_IN_SECONDS)):
            return True
        return False
    
    @property
    def is_domain_enabled(self):
        if self.can_update_slug():
            return False
        return True
    
    def update_slug(self, new_slug_name):
        '''Ensuring slug cant be updated more than once'''
        if self.can_update_slug():
            self.slug = new_slug_name
            self.save()
            return
        raise CantUpdateSlugAgainException

    def check_password(self, password):
        return self.user.check_password(password)
    
    def update_password(self, new_password):
        self.user.set_password(new_password)
        self.user.save()
    
    set_password = update_password 
    
    @property
    def all_notes(self):
        return self.note_set.values('id', 'name', 'public').all()
    
    @property
    def public_notes(self):
        return self.note_set.filter(public=True).values('id', 'name', 'note').all()
    
    def is_my_note(self, note):
        return bool(self.note_set.filter(id=note.id).count())
    
    @property
    def domain(self):
        if not self.slug:
            return ''
        return ".".join([self.slug, Site.objects.get(id=settings.SITE_ID).domain])
    
    @property
    def achievements(self):
        return self.achievement_set.values('id', 'title', 'description')
    
class CollegeAlreadyExistsException(Exception):
    pass

class CollegeManager(BaseModelManager):
    def create_college(self, name):
        slug = slugify(name)
        if self.exists(slug=slug):
            raise CollegeAlreadyExistsException
        college = College(name=name, slug=slug)
        college.save()
        return college 
            
class College(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, db_index=True)#this will be used as its unique url identifier
    objects = CollegeManager()
    
    def __unicode__(self):
        return self.name
    
    @property
    def students(self):
        userprofiles_ids = self.acadinfo_set.values('userprofile')
        return UserProfile.objects.filter(id__in=[id['userprofile'] for id in userprofiles_ids]).values('id', 'slug', 'name')
    
class CompanyAlreadyExistsException(Exception):
    pass

class CompanyManager(BaseModelManager):
    def create_company(self, name):
        slug = slugify(name)
        if self.exists(slug=slug):
            raise CompanyAlreadyExistsException
        company = Company(name=name, slug=slug)
        company.save()
        return company
    
class Company(BaseModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, db_index=True)#this will be used as its unique url identifier
    objects = CompanyManager()
    
    def __unicode__(self):
        return self.name
    
    @property
    def employees(self):
        content_type = ContentType.objects.get(name='company')
        userprofiles_ids = WorkInfo.objects.filter(content_type=content_type, object_id=self.id).values('userprofile')
        return UserProfile.objects.filter(id__in=[id['userprofile'] for id in userprofiles_ids]).values('id', 'slug', 'name')
    
class WorkInfoAlreadyExistsException(Exception):
    pass
    
class WorkInfoManager(BaseModelManager):
    def create_workinfo(self, userprofile, workplace, designation, years_of_exp):
        if self.exists(userprofile=userprofile):
            raise WorkInfoAlreadyExistsException
        workinfo = WorkInfo(userprofile=userprofile,
                            workplace=workplace,
                            designation=designation,
                            years_of_exp=years_of_exp)
        workinfo.save()
        return workinfo
    
class WorkInfo(BaseModel):
    userprofile = models.ForeignKey(UserProfile)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    workplace = generic.GenericForeignKey()
    designation = models.CharField(max_length=50, blank=True, null=True)
    years_of_exp = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    objects = WorkInfoManager()
    
    def __unicode__(self):
        return '%s (%s)' % (self.userprofile.name, self.workplace.name)

class AcadInfoAlreadyExistsException(Exception):
    pass
    
class AcadInfoManager(BaseModelManager):
    def create_acadinfo(self, userprofile, branch, college, start_year, end_year, aggregate):
        if self.exists(userprofile=userprofile):
            raise AcadInfoAlreadyExistsException
        if branch or college or start_year or end_year or aggregate:
            acadinfo = AcadInfo(userprofile=userprofile,
                                    branch=branch,
                                    college=college,
                                    start_year=start_year,
                                    end_year=end_year,
                                    aggregate=aggregate)
            acadinfo.save()
            return acadinfo

class AcadInfo(BaseModel):
    userprofile = models.ForeignKey(UserProfile)
    branch = models.CharField(choices=branches, max_length=4, blank=True, null=True)
    college = models.ForeignKey(College)
    start_year = YearField(max_length=4, blank=True, null=True)
    end_year = YearField(max_length=4, blank=True, null=True)
    aggregate = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    objects = AcadInfoManager()
    
    def __unicode__(self):
        return "%s-(%s-%s-%s)-%s" % (self.userprofile, self.branch, self.start_year, self.end_year, self.aggregate)
    
class NoteManager(BaseModelManager):
    def create_note(self, userprofile, name, note, short_description='', public=True):
        note = Note(userprofile=userprofile,
                     name=name,
                     short_description=short_description,
                     note=note,
                     public=public)
        note.save()
        return note
    
class Note(BaseModel):
    userprofile = models.ForeignKey(UserProfile)
    name = models.CharField(max_length=30)
    short_description = models.CharField(max_length=50)
    note = models.CharField(max_length=7000)
    public = models.BooleanField(default=True)
    objects = NoteManager()
    
    def __unicode__(self):
        return "%s..." % self.note[:10]
    
class AchievementAlreadyExistsException(Exception):
    pass

class AchievementManager(BaseModelManager):
    def create_achievement(self, userprofile, title, description=''):
        if self.exists(userprofile=userprofile, title=title):
            raise AchievementAlreadyExistsException
        achievement = Achievement(userprofile=userprofile,
                                  title=title,
                                  description=description)
        achievement.save()
        return achievement
    
class Achievement(BaseModel):
    userprofile = models.ForeignKey(UserProfile)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=7000)
    objects = AchievementManager()
    
    def __unicode__(self):
        return "%s..." % self.title[:10]