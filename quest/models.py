from django.db import models
from utils.models import BaseModel, BaseModelManager
from utils import slugify
from users.models import UserProfile

class QuestionAlreadyExistsException(Exception):
    pass

class AnswerCantBeAcceptedException(Exception):
    pass

class AnsweringIsClosedException(Exception):
    pass

class QuestionManager(BaseModelManager):
    def create_question(self, title, description, userprofile):
        if self.exists(title=title):
            raise QuestionAlreadyExistsException
        question = Question(title=title, slug=slugify(title),
                            description=description, raised_by=userprofile)
        question.save()
        return question 
            
    def exists(self, title):
        if self.filter(slug=slugify(title)).count():
            return True
        return False
    
class Question(BaseModel):
    title = models.CharField(max_length=80, blank=False)
    slug = models.SlugField(max_length=80, db_index=True)
    description = models.CharField(max_length=1000, blank=True, null=True)#should clean tags.
    raised_by = models.ForeignKey(UserProfile)
    closed = models.BooleanField(default=False)
    objects = QuestionManager()
    
    def __unicode__(self):
        return "%s...." % self.title[:10]
    
    @property
    def answers(self):
        return self.answer_set.all()
    
    @property
    def owner(self):
        return self.raised_by
    
    @property
    def accepted_answer(self):
        if self.answers.filter(accepted=True).count():#since lazy fetching is allowed
            return self.answers.get(accepted=True)#there will only be one accepted answer for a question
        return None
    
    def close_answering(self):
        if not self.closed:
            self.closed = True
            self.save()
    
    def is_accepting_answers(self):
        if self.closed:
            return False
        return True 
    
class AnswerManager(BaseModelManager):
    def create_answer(self, question, description, userprofile, accepted=False):
        if question.closed:
            raise AnsweringIsClosedException
        if accepted and (question.raised_by.id != userprofile.id):
            raise AnswerCantBeAcceptedException
        if accepted:
            for previous_answer in question.answer_set.all():
                previous_answer.unaccept()
        answer = Answer(question=question,
                        description=description,
                        accepted=accepted,
                        given_by=userprofile)
        answer.save()
        return answer
    
class Answer(BaseModel):
    question = models.ForeignKey(Question)
    description = models.CharField(max_length=2000, blank=True, null=True)
    accepted = models.BooleanField(default=False)
    given_by = models.ForeignKey(UserProfile)
    objects = AnswerManager()
    
    def __unicode__(self):
        return "%s...." % self.description[:10]
    
    def unaccept(self):
        if self.accepted:
            self.accepted = False
            self.save()
    
    def accept(self, accepted_by):
        if not self.accepted:
            if self.question.raised_by.id != accepted_by.id:
                raise AnswerCantBeAcceptedException
            all_answers_for_the_question = self.question.answer_set.all()
            for answer in all_answers_for_the_question:
                answer.unaccept()
            self.accepted = True
            self.save()