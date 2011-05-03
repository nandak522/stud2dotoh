from django.db import models
from utils.models import BaseModel, BaseModelManager
from utils import slugify
from users.models import UserProfile
from taggit.managers import TaggableManager
from django.db.models.signals import post_save
from django.conf import settings

class QuestionAlreadyExistsException(Exception):
    pass

class AnswerCantBeAcceptedException(Exception):
    pass

class AnsweringIsClosedException(Exception):
    pass

class EmptyQuestionCantBeSavedException(Exception):
    pass

class QuestionManager(BaseModelManager):
    def create_question(self, title, description, userprofile, tags):
        if self.exists(slug=slugify(title)):
            raise QuestionAlreadyExistsException
        question = Question(title=title, slug=slugify(title),
                            description=description, raised_by=userprofile)
        question.save()
        question.tags.add(*tags)
        return question 
            
    def update_question(self, question, **attributes):
        if attributes:
            if attributes.has_key('title') and attributes.has_key('description') and attributes.get('title') and attributes.get('description'):
                if attributes.has_key('tags'):
                    tags = attributes.get('tags')
                    question.tags.clear()
                    question.tags.add(*tags)
                attributes.pop('tags')
                for attr_label in attributes:
                    setattr(question, attr_label, attributes[attr_label])
                question.save()
                return 
        raise EmptyQuestionCantBeSavedException
    
class Question(BaseModel):
    title = models.CharField(max_length=80)
    slug = models.SlugField(max_length=80, db_index=True)
    description = models.CharField(max_length=1000, blank=True, null=True)#should clean tags.
    raised_by = models.ForeignKey(UserProfile)
    closed = models.BooleanField(default=False)
    objects = QuestionManager()
    tags = TaggableManager()
    
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
    
    def all_related_users_emails(self):
        emails = []
        emails.append(self.raised_by.user.email)
        for answer in self.answers:
            emails.append(answer.given_by.user.email)
        return set(emails)
    
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
            
def increment_question_points(sender, instance, **kwargs):
    if kwargs['created']:
        userprofile = instance.raised_by
        userprofile.add_points(settings.QUESTION_POINTS)

def increment_answer_points(sender, instance, **kwargs):
    if kwargs['created']:
        userprofile = instance.given_by 
        userprofile.add_points(settings.ANSWER_POINTS)
            
post_save.connect(increment_question_points, Question, dispatch_uid='increment_question_signal')
post_save.connect(increment_answer_points, Answer, dispatch_uid='increment_answer_signal')
