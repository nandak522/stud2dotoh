from utils import TestCase
from quest.forms import AskQuestionForm, GiveAnswerForm

class AskQuestionFormTests(TestCase):
    def test_valid_ask_question(self):
        form_data = {'title':'How do we handle recursion in Python',
                     'description':'I am a newbee to Python. Can you share me ways to handle recurion in python ?'}
        form = AskQuestionForm(form_data)
        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)

    def test_invalid_ask_question(self):
        form_data = {'title':'', 'description':''}
        form = AskQuestionForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.has_key('title'))
        self.assertTrue(form.errors.has_key('description'))

class GiveAnswerFormTests(TestCase):
    def test_valid_give_answer(self):
        form_data = {'description':'This is how you handle recurion in python:'}
        form = GiveAnswerForm(form_data)
        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)

    def test_invalid_give_answer(self):
        form_data = {'description':''}
        form = GiveAnswerForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.has_key('description'))