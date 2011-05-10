from haystack.indexes import *
from haystack import site
from quest.models import Question

class QuestionIndex(SearchIndex):
    title = CharField(document=True, use_template=True)

    def index_queryset(self):
       return Question.objects.all()
