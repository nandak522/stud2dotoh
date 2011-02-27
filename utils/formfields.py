from django import forms
from utils.emailer import EMAIL_REGEX
from django.core.exceptions import ValidationError

class MultipleEmailsField(forms.CharField):
    def clean(self, value):
        value = super(MultipleEmailsField, self).to_python(value)
        if not value and self.required:
            raise ValidationError(self.error_messages['required'])
        return value
    
class AutocompleteWidget(forms.TextInput):
    class Media:
        css = {'all':('/site_media/js/jquery/plugins/autocomplete/jquery-autocomplete/jquery.autocomplete.css',)}
        js = ('/site_media/js/jquery/plugins/autocomplete/jquery-autocomplete/jquery.autocomplete-min.js',)    