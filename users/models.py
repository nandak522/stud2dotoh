from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from utils.models import BaseModel, BaseModelManager

class UserProfileAlreadyExistsException(Exception):
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

    def __unicode__(self):
        return self.email
    
    def check_password(self, password):
        return self.user.check_password(password)
