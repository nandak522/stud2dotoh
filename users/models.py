from django.contrib.auth.models import User
from django.db import models
from utils import slugify
from utils.models import BaseModel, BaseModelManager, YearField
from django.conf import settings
from datetime import timedelta
import os
import hashlib

branches = (('CSE', 'Computer Science Engineering'),)

class UserProfileAlreadyExistsException(Exception):
    pass

class CantUpdateSlugAgainException(Exception):
    pass

class UserProfileManager(BaseModelManager):
    def create_profile(self, email, password, name):
        if self.exists(email=email):
            raise UserProfileAlreadyExistsException
        user = User.objects.create_user(username=self._compute_username(email),
                                        email=email,
                                        password=password)
        userprofile = UserProfile(user=user, name=name, slug=slugify(name))
        userprofile.save()
        return userprofile
    
    def _compute_username(self, email):
        return hashlib.sha1(email).hexdigest()[:30]
    
    def exists(self, email=''):
        try:
            self.get(user__email=email)
            return True
        except UserProfile.DoesNotExist:
            return False

class UserProfile(BaseModel):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(max_length=50, db_index=True, unique=True)#this will be used as his unique url identifier
    objects = UserProfileManager()
    
    def update(self, **kwargs):
        if 'password' in kwargs.keys():
            self.update_password(kwargs['password'])
            kwargs.pop('password')
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
        if self.exists(slug):
            raise CollegeAlreadyExistsException
        college = College(name=name,slug=slug)
        college.save()
        return college 
            
    def exists(self, slug):
        try:
            return self.get(slug=slug)
        except College.DoesNotExist:
            return False

class College(BaseModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, db_index=True)#this will be used as its unique url identifier
    objects = CollegeManager()
    
    def __unicode__(self):
        return self.name
    
class ProfessorAlreadyExistsException(Exception):
    pass
    
class ProfessorManager(BaseModelManager):
    def create_professor(self, userprofile, college):
        if self.exists(userprofile):
            raise ProfessorAlreadyExistsException
        professor = Professor(userprofile=userprofile, college=college)
        professor.save()
        return professor
    
    def exists(self, userprofile):
        try:
            return self.get(userprofile=userprofile)
        except Professor.DoesNotExist:
            return False
    
class Professor(BaseModel):
    userprofile = models.ForeignKey(UserProfile)
    college = models.ForeignKey(College)
    objects = ProfessorManager()
    
    def __unicode__(self):
        return "%s-(%s)" % (self.userprofile.name, self.college.name)
    
#class IndustryGuy(UserProfile):
#    raise NotImplementedError
#
#class Company(BaseModel):
#    raise NotImplementedError
#
    
class StudentAlreadyExistsException(Exception):
    pass
    
class StudentManager(BaseModelManager):
    def create_student(self, userprofile, branch, college, start_year, end_year):
        if self.exists(userprofile):
            raise StudentAlreadyExistsException
        student = Student(userprofile=userprofile,
                          branch=branch,
                          college=college,
                          start_year=start_year,
                          end_year=end_year)
        student.save()
        return student
            
    def exists(self, userprofile):
        try:
            return self.get(userprofile=userprofile)
        except Student.DoesNotExist:
            return False

class Student(BaseModel):
    userprofile = models.ForeignKey(UserProfile)
    branch = models.CharField(choices=branches, max_length=4)
    college = models.ForeignKey(College)
    start_year = YearField(max_length=4, blank=True, null=True)
    end_year = YearField(max_length=4, blank=True, null=True)
    objects = StudentManager()
    
    def __unicode__(self):
        return "%s-(%s-%s-%s)" % (self.userprofile, self.branch, self.start_year, self.end_year)