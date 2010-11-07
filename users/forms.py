from django import forms
import re
from users.models import UserProfile
from django.core.exceptions import ValidationError

USERNAME_FILTER_REGEX = '[^a-zA-Z0-9]'
FILENAME_FILTER_REGEXT = '[^\.]'

class UserSignupForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput())
    name = forms.CharField(max_length=50, required=False)
    email = forms.EmailField(max_length=50, required=False)
    next_url = forms.CharField(max_length=128, required=False, widget=forms.HiddenInput())

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username == re.sub(r'%s' % USERNAME_FILTER_REGEX, '', username):
            try:
                UserProfile.objects.get(user__username=username)
                raise ValidationError('Username Already Picked!')
            except UserProfile.DoesNotExist:
                return username
        else:
            raise ValidationError('Username should only contain alphabets and digits!')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            UserProfile.objects.get(user__email=email)
            raise ValidationError('Email Already Picked!')
        except UserProfile.DoesNotExist:
            return email

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput())
    next_url = forms.CharField(max_length=128, required=False, widget=forms.HiddenInput())

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username == re.sub(r'%s' % USERNAME_FILTER_REGEX, '', username):
            try:
                UserProfile.objects.get(user__username=username)
                return username
            except UserProfile.DoesNotExist:
                raise ValidationError('Invalid Username!')
        raise ValidationError('Invalid Username! Username should only be alphabetic. a-z,A-Z,0-9')
    
class SaveFileForm(forms.Form):
    name = forms.CharField(max_length=30, required=True)
    short_description = forms.CharField(max_length=50, required=False)
    content = forms.CharField(max_length=7000, required=True,widget=forms.Textarea())
    public = forms.BooleanField(required=False, initial=True)
    
    def clean_content(self):
        return self.cleaned_data.get('content').strip()