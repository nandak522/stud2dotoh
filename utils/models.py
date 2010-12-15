from django.db import models
from django.db.models import Manager as BaseModelManager
from django.db.models import IntegerField
from django.core import exceptions
from datetime import datetime

class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_on']
        get_latest_by = 'created_on'
        
class YearField(IntegerField):
    def validate(self, value, model_instance):
        if value < 1910:
            raise exceptions.ValidationError, 'Year can\'t be less than 1910'
        present_year = datetime.today().year
        if value > present_year:
            raise exceptions.ValidationError, 'Year can\'t be less than %s' % present_year
        return