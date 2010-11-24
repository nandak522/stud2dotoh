from django import forms

class AskQuestionForm(forms.Form):
    title = forms.CharField(max_length=80, required=True)
    description = forms.CharField(max_length=1000, required=True, widget=forms.Textarea(attrs={'rows':10, 'cols':50}))
    
class GiveAnswerForm(forms.Form):
    description = forms.CharField(max_length=2000, required=True, widget=forms.Textarea(attrs={'rows':10, 'cols':50}))