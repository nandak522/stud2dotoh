from django import forms
from django.template.defaultfilters import removetags
from django.conf import settings

class AskQuestionForm(forms.Form):
    title = forms.CharField(max_length=80, required=True)
    description = forms.CharField(max_length=1000, required=True, widget=forms.Textarea(attrs={'rows':10, 'cols':50}))
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        return removetags(description, settings.FILTER_HTML_TAGS)
    
class GiveAnswerForm(forms.Form):
    description = forms.CharField(max_length=2000, required=True, widget=forms.Textarea(attrs={'rows':10, 'cols':100, 'width':'300px'}))
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        return removetags(description, settings.FILTER_HTML_TAGS)