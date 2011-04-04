from django import forms
from utils.emailer import EMAIL_REGEX
from django.core.exceptions import ValidationError
from taggit.forms import TagField as DefaultTagField, TagWidget
from taggit.utils import parse_tags
import re

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
        
class TagField(DefaultTagField):
    widget = TagWidget

    def clean(self, value):
        tags = super(TagField, self).clean(value)
        cleaned_tags = tags_cleanup(tags)

def tags_cleanup(tags):
    if isinstance(tags, str):
        tags = tags.split(',')
    cleaned_tags = []
    for tag in tags:
        cleaned_tags.append(re.sub(r'(\s)', '-', tag.lower().strip()))
    return tuple(cleaned_tags)