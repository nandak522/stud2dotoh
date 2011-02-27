from django import forms
from django.core.exceptions import ValidationError
from users.models import UserProfile, branches
import re
from users.messages import USER_LOGIN_FAILURE
from utils.formfields import MultipleEmailsField

USER_NAME_CLEANUP_REGEX_PATTERN = re.compile(r'[^\w.&\s-]+', re.IGNORECASE)
USER_SLUG_DOMAIN_CLEANUP_REGEX_PATTERN = re.compile(r'stud2dotoh.com', re.IGNORECASE)
USER_SLUG_CLEANUP_REGEX_PATTERN = re.compile(r'[^a-zA-Z0-9]', re.IGNORECASE)
COLLEGE_NAME_CLEANUP_REGEX_PATTERN = re.compile(r'[^\w.&\s-]+', re.IGNORECASE) 
FILENAME_FILTER_REGEXT = '[^.]'
MIN_COLLEGE_START_YEAR = 1910
MIN_COLLEGE_END_YEAR = 1912
MAX_COLLEGE_START_YEAR = 2011
MAX_COLLEGE_END_YEAR = 2015
COLLEGE_START_YEAR_RANGE = tuple([(year, year) for year in range(MIN_COLLEGE_START_YEAR, MAX_COLLEGE_START_YEAR+1)]) 
COLLEGE_END_YEAR_RANGE = tuple([(year, year) for year in range(MIN_COLLEGE_END_YEAR, MAX_COLLEGE_END_YEAR+1)])
YEARS_OF_EXP_CLEANUP_REGEX_PATTERN = re.compile(r'^\d+([\.]\d[\d]*)*$')

class UserSignupForm(forms.Form):
    email = forms.EmailField(max_length=50, required=True)
    password = forms.CharField(min_length=6, max_length=50, required=True, widget=forms.PasswordInput())
    name = forms.CharField(max_length=50, required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            UserProfile.objects.get(user__email=email)
            raise ValidationError('Email Already Picked!')
        except UserProfile.DoesNotExist:
            return email
        
class StudentSignupForm(UserSignupForm):
    college = forms.CharField(required=True, max_length=100)
    
class EmployeeSignupForm(UserSignupForm):
    company = forms.CharField(required=True, max_length=50)
    
class ProfessorSignupForm(UserSignupForm):
    college = forms.CharField(required=True, max_length=100)

class UserLoginForm(forms.Form):
    email = forms.EmailField(max_length=50, required=True)
    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput())
    
class SaveNoteForm(forms.Form):
    name = forms.CharField(max_length=30, required=True)
    short_description = forms.CharField(max_length=50, required=False)
    content = forms.CharField(max_length=7000, required=True,widget=forms.Textarea())
    public = forms.BooleanField(required=False, initial=True)
    
    def clean_content(self):
        return self.cleaned_data.get('content').strip()
    
class PersonalSettingsForm(forms.Form):
    name = forms.CharField(max_length=50, required=True)
    slug = forms.CharField(max_length=50, required=False)
    new_password = forms.CharField(max_length=50, required=False, widget=forms.PasswordInput())
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise ValidationError('Please Enter a Valid Name')
        name = re.sub(USER_NAME_CLEANUP_REGEX_PATTERN, '', name)
        if not name.strip():
            raise ValidationError('Please Enter a Valid Name')
        return name
    
    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        slug = re.sub(USER_SLUG_DOMAIN_CLEANUP_REGEX_PATTERN, '', slug)
        if slug == re.sub(USER_SLUG_CLEANUP_REGEX_PATTERN, '', slug):
            return slug
        raise ValidationError('Please choose a Valid Web Resume Url. Should only contain alphabets and/or numbers')
    
    def masquerade_slug(self):
        #TODO:The goal is to show editable slug field only once.
        #so {{form.slug}} should be dynamic enough to render as a 
        #editable text field first time and as a simple label from second time.  
        raise NotImplementedError

class AcadSettingsForm(forms.Form):
    branch = forms.ChoiceField(required=True, choices=branches)
    college = forms.CharField(required=True, max_length=100)
    start_year = forms.ChoiceField(required=False, choices=COLLEGE_START_YEAR_RANGE, initial=(2007, 2007))
    end_year = forms.ChoiceField(required=False, choices=COLLEGE_END_YEAR_RANGE, initial='2011')
    
    def clean_college(self):
        college = self.cleaned_data.get('college')
        cleaned_college = re.sub(COLLEGE_NAME_CLEANUP_REGEX_PATTERN, '', college)
        if college != cleaned_college:
            raise ValidationError('Please choose a Valid college name. It cannot contain special symbols other than dot, hyphen, underscore')
        return cleaned_college

class WorkInfoSettingsForm(forms.Form):
    workplace = forms.CharField(required=True, max_length=100)
    designation = forms.CharField(required=False, max_length=50)
    years_of_exp = forms.CharField(required=False, max_length=5)
    
    def clean_workplace(self):
        workplace = self.cleaned_data.get('workplace')
        cleaned_workplace = re.sub(COLLEGE_NAME_CLEANUP_REGEX_PATTERN, '', workplace)
        if workplace != cleaned_workplace:
            raise ValidationError('Please choose a Valid Work Place name. It cannot contain special symbols other than dot, hyphen, underscore')
        return cleaned_workplace
    
    def clean_years_of_exp(self):
        years_of_exp = self.cleaned_data.get('years_of_exp')
        if re.match(YEARS_OF_EXP_CLEANUP_REGEX_PATTERN, years_of_exp):
            return years_of_exp
        raise ValidationError('Please enter Valid years of Experience. It should be of the format YY.MM')
    
class ContactForm(forms.Form):
    subject = forms.CharField(required=False,max_length=100)
    message = forms.CharField(max_length=500, required=True,widget=forms.Textarea())
    
class ContactUserForm(ContactForm):
    to = forms.EmailField(max_length=50, required=True, widget=forms.TextInput(attrs={'readonly':True}))

class ContactGroupForm(ContactForm):
    to = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'readonly':True}))
    
class ContactUsForm(ContactForm):
    from_name = forms.CharField(required=False,max_length=50)
    from_email = forms.EmailField(max_length=50, required=True)
    
class InvitationForm(forms.Form):
    to_emails = MultipleEmailsField(max_length=500, required=True)
    
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(required=True, max_length=50)
    
class ResetMyPasswordForm(forms.Form):
    password = forms.CharField(min_length=6, max_length=50, required=True, widget=forms.PasswordInput())