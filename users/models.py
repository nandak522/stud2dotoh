from django.contrib.auth.models import User
from django.db import models
from utils import slugify
from utils.models import BaseModel, BaseModelManager
from django.conf import settings
from datetime import timedelta
import os

class UserProfileAlreadyExistsException(Exception):
    pass

class CantUpdateSlugAgainException(Exception):
    pass

class UserProfileManager(BaseModelManager):
    def create_userprofile(self, username, password, email='', name=''):
        if self.exists(username=username, email=email):
            raise UserProfileAlreadyExistsException
        user = User.objects.create_user(username=username,
                                        email=email,
                                        password=password)
        userprofile = UserProfile(user=user, name=name, slug=slugify(name))
        userprofile.save()
        return userprofile
    
    def exists(self, username, email=''):
        if not email:
            try:
                self.get(user__username=username)
                return True
            except UserProfile.ModelDoesNotExist:
                return False
        try:
            self.get(user__username=username, user__email=email)
            return True
        except UserProfile.DoesNotExist:
            return False

class UserProfile(BaseModel):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(max_length=50, db_index=True)#this will be used as his unique url identifier
    objects = UserProfileManager()
    
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
        return True
    
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