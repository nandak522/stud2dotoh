from django.db import models
from utils.models import BaseModel, BaseModelManager
from utils import slugify

class QuestionAlreadyExistsException(Exception):
    pass

class QuestionManager(BaseModelManager):
    def create_question(self, title, description):
        if self.exists(title=title):
            raise QuestionAlreadyExistsException
        question = Question(title=title, slug=slugify(title), description=description)
        question.save()
        return question 
            
    def exists(self, title):
        if self.filter(title=slugify(title)).count():
            return True
        return False

class Question(BaseModel):
    title = models.CharField(max_length=80, blank=False)
    slug = models.SlugField(max_length=80, db_index=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    
    def __unicode__(self):
        return self.title