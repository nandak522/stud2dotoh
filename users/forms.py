from django import forms
import re

class UserSignupForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    email = forms.CharField(max_length=50, required=False)
    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput())
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username == re.sub(r'[\w]+', '', username):
            return True
        return False