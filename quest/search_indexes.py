from haystack import indexes
from haystack import site
from quest.models import Question

class QuestionIndex(indexes.RealTimeSearchIndex):
    title = indexes.CharField(document=True, use_template=True, model_attr='title')

site.register(Question, QuestionIndex)
