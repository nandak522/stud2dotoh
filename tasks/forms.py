from django import forms
from django.forms.widgets import Textarea, HiddenInput

class TaskSolutionForm(forms.Form):
    task_id = forms.CharField(widget=HiddenInput())
    solution = forms.CharField(widget=Textarea(attrs={'rows':10, 'cols':100}),
                               required=True)
