from django import forms
import re
from users.models import UserProfile
from django.core.exceptions import ValidationError

USERNAME_FILTER_REGEX = '[^\w]'

class UserSignupForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=50, required=False)
    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username == re.sub(r'%s' % USERNAME_FILTER_REGEX, '', username):
            try:
                UserProfile.objects.get(user__username=username)
                raise ValidationError('Username Already Picked!')
            except UserProfile.DoesNotExist:
                return username
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            UserProfile.objects.get(user__email=email)
            raise ValidationError('Email Already Picked!')
        except UserProfile.DoesNotExist:
            return True

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username == re.sub(r'%s' % USERNAME_FILTER_REGEX, '', username):
            try:
                UserProfile.objects.get(user__username=username)
                return username
            except UserProfile.DoesNotExist:
                raise ValidationError('Invalid Username!')
        raise ValidationError('Invalid Username! Username should only be alphabetic. a-z,A-Z,0-9')