from utils import TestCase
from quest.models import Question, Answer

class QuestionCreationTests(TestCase):
    fixtures = ['users.json']

    def test_question_valid_creation(self):
        raise NotImplementedError
    
    def test_creating_duplicate_questions(self):
        raise NotImplementedError
    
class AnswerCreationTests(TestCase):
    fixtures = ['users.json']
    
    def test_valid_answer_creation(self):
        raise NotImplementedError
    
    def test_creating_duplicate_answers(self):
        raise NotImplementedError
    
    def test_accepting_an_answer(self):
        raise NotImplementedError
    
    def test_accepting_more_than_one_answer(self):
        raise NotImplementedError
    
    def test_accepting_answer_by_nonowner_of_a_question(self):
        raise NotImplementedError
    
    def test_unaccepting_an_answer(self):
        raise NotImplementedError
    
    def test_retrieving_all_answers_for_a_question(self):
        raise NotImplementedError