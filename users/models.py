from datetime import timedelta
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db import connection
from utils import slugify
from utils.models import BaseModel, BaseModelManager, YearField
import hashlib
import os

branches = (('CSE', 'Computer Science Engineering'),)

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
    slug = models.SlugField(max_length=50, db_index=True, unique=True)#this will be used as his unique url identifier
    objects = UserProfileManager()
    
    def make_student(self):
        self.user.groups.add(Group.objects.get(name='Student'))
        
    def make_employee(self):
        self.user.groups.add(Group.objects.get(name='Employee'))
        
    def make_professor(self):
        self.user.groups.add(Group.objects.get(name='Professor'))
    
    @property    
    def is_student(self):
        return Group.objects.get(name="Student") in self.user.groups.all() 
        
    @property
    def is_professor(self):
        return Group.objects.get(name="Professor") in self.user.groups.all()
        
    @property
    def is_employee(self):
        return Group.objects.get(name="Employee") in self.user.groups.all()
    
    def join_college(self, college_name):
        college_slug = slugify(college_name)
        if College.objects.exists(slug=college_slug):
            college = College.objects.get(slug=college_slug)
        else:
            college = College.objects.create_college(name=college_name)
        AcademicInfo.objects.create_academicinfo(self, branch='', college=college, start_year='', end_year='')
    
    @property
    def acad_details(self):
        acad_details = self.acadinfo_set
        if acad_details.count():
            return acad_details.all()[0]
        return None
        
    @property
    def work_details(self):
        work_details = self.workinfo_set
        if work_details.count():
            return work_details.values('workplace', 'designation', 'years_of_exp')[0]
        return ('',)
        
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
        if self.modified_on <= (self.created_on+timedelta(minutes=1)):
            return True
        return False
    
    def update_slug(self, new_slug_name):
        '''Ensuring slug cant be updated more than once'''
        if self.can_update_slug():
            self.slug = new_slug_name
            self.save()
            return
        raise CantUpdateSlugAgainException

    def __unicode__(self):
        return self.name
    
    def check_password(self, password):
        return self.user.check_password(password)
    
    def update_password(self, new_password):
        self.user.set_password(new_password)
        self.user.save()
    
    set_password = update_password 
    
    @property
    def user_directory_path(self):
        return "/".join([settings.DOCSTORE_CONFIG['files_storage_path'], str(self.id)])
    
    @property
    def public_uploaded_files(self):
        #TODO:For now all uploaded files are public by default.
        return self.all_uploaded_files
    
    @property
    def all_uploaded_files(self):
        user_directory_path = self.user_directory_path
        if settings.DOCSTORE_CONFIG['local']:
            if os.path.exists(user_directory_path):
                return tuple(os.walk(user_directory_path).next()[-1])
        else:
            raise NotImplementedError
        return ()

    @property
    def domain(self):
        if not self.slug:
            return ''
        return ".".join([self.slug, 'stud2dotoh.com'])
    
class CollegeAlreadyExistsException(Exception):
    pass

class CollegeManager(BaseModelManager):
    def create_college(self, name):
        slug=slugify(name)
        if self.exists(slug=slug):
            raise CollegeAlreadyExistsException
        college = College(name=name,slug=slug)
        college.save()
        return college 
            
class College(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, db_index=True)#this will be used as its unique url identifier
    objects = CollegeManager()
    
    def __unicode__(self):
        return self.name
    
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
    designation = models.CharField(max_length=50)
    years_of_exp = models.DecimalField(max_digits=4, decimal_places=2)
    objects = WorkInfoManager()
    
    def __unicode__(self):
        return '%s (%s)' % (self.userprofile.name, self.company.name)

class AcadInfoAlreadyExistsException(Exception):
    pass
    
class AcadInfoManager(BaseModelManager):
    def create_acadinfo(self, userprofile, branch, college, start_year, end_year):
        if self.exists(userprofile=userprofile):
            raise AcadInfoAlreadyExistsException
        if branch or college or start_year or end_year:
            acadinfo = AcadInfo(userprofile=userprofile,
                                    branch=branch,
                                    college=college,
                                    start_year=start_year,
                                    end_year=end_year)
            acadinfo.save()
            return acadinfo

class AcadInfo(BaseModel):
    userprofile = models.ForeignKey(UserProfile)
    branch = models.CharField(choices=branches, max_length=4, blank=True, null=True)
    college = models.ForeignKey(College)
    start_year = YearField(max_length=4, blank=True, null=True)
    end_year = YearField(max_length=4, blank=True, null=True)
    objects = AcadInfoManager()
    
    def __unicode__(self):
        return "%s-(%s-%s-%s)" % (self.userprofile, self.branch, self.start_year, self.end_year)