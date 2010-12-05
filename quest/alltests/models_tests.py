from utils import TestCase
from users.models import UserProfile
from quest.models import Question, Answer, QuestionAlreadyExistsException, AnswerCantBeAcceptedException, AnsweringIsClosedException,EmptyQuestionCantBeSavedException

class QuestionCreationTests(TestCase):
    fixtures = ['users.json']

    def test_question_valid_creation(self):
        question_data = {'title':'What are the best companies working on Python ?',
                         'description':'<a href="http://google.com/">Google</a>, <a href="http://hp.com/">HP</a>',
                         'raised_by':UserProfile.objects.latest()}
        Question.objects.create_question(title=question_data['title'],
                                         description=question_data['description'],
                                         userprofile=question_data['raised_by'])
        question = Question.objects.latest()
        self.assertTrue(question)
        self.assertEquals(question.title, question_data['title'])
        self.assertEquals(question.description, question_data['description'])
        self.assertEquals(question.raised_by.id, question_data['raised_by'].id)
        self.assertFalse(question.closed)
    
    def test_creating_duplicate_questions(self):
        question_data = {'title':'What are the best companies working on Python ?',
                         'description':'<a href="http://google.com/">Google</a>, <a href="http://hp.com/">HP</a>',
                         'raised_by':UserProfile.objects.latest()}
        Question.objects.create_question(title=question_data['title'],
                                         description=question_data['description'],
                                         userprofile=question_data['raised_by'])
        question = Question.objects.latest()
        self.assertTrue(question)
        self.assertRaises(QuestionAlreadyExistsException,
                          Question.objects.create_question,
                          title=question_data['title'],
                          description=question_data['description'],
                          userprofile=question_data['raised_by'])
    
    def test_close_answering(self):
        question_data = {'title':'What are the best companies working on Python ?',
                         'description':'<a href="http://google.com/">Google</a>, <a href="http://hp.com/">HP</a>',
                         'raised_by':UserProfile.objects.latest()}
        Question.objects.create_question(title=question_data['title'],
                                         description=question_data['description'],
                                         userprofile=question_data['raised_by'])
        question = Question.objects.latest()
        self.assertTrue(question)
        self.assertFalse(question.closed)
        question.close_answering()
        self.assertTrue(question.closed)
        
class QuestionUpdatingTests(TestCase):
    fixtures = ['questions.json']
    
    def test_update_question_with_empty_content(self):
        question = Question.objects.latest()
        self.assertRaises(EmptyQuestionCantBeSavedException,
                          Question.objects.update_question,
                          question)
        self.assertRaises(EmptyQuestionCantBeSavedException,
                          Question.objects.update_question,
                          question,
                          title='',
                          description='')
        modified_question = Question.objects.get(id=question.id)
        self.assertEquals(modified_question.title, question.title)
        self.assertEquals(modified_question.description, question.description)
    
    def test_update_question_with_valid_content(self):
        question = Question.objects.latest()
        question_previous_info = {'title':question.title,
                                  'description':question.description} 
        updated_info = {'title':"Title is updated",
                        'description':"Description is updated"}
        Question.objects.update_question(question, title=updated_info['title'], description=updated_info['description'])
        modified_question = Question.objects.get(id=question.id)
        self.assertNotEquals(modified_question.title, question_previous_info['title'])
        self.assertNotEquals(modified_question.description, question_previous_info['description'])
        self.assertEquals(modified_question.title, updated_info['title'])
        self.assertEquals(modified_question.description, updated_info['description'])
        
class AnswerCreationTests(TestCase):
    fixtures = ['users.json', 'questions.json', 'answers.json']
    
    def test_valid_answer_creation(self):
        question = Question.objects.latest()
        answer_data = {'question':question,
                       'description':'There are many ways to handle recursion',
                       'accepted':False,
                       'given_by':UserProfile.objects.latest()}
        Answer.objects.create_answer(question=answer_data['question'],
                                     description=answer_data['description'],
                                     accepted=answer_data['accepted'],
                                     userprofile=answer_data['given_by'])
        answer = Answer.objects.latest()
        self.assertTrue(answer)
        self.assertEquals(answer.question.id, question.id)
        self.assertEquals(answer.description, answer_data['description'])
        self.assertFalse(answer.accepted)
        self.assertEquals(answer.given_by.id, answer_data['given_by'].id)
        self.assertTrue(answer in question.answers)
    
    def test_creating_duplicate_answers(self):
        question = Question.objects.latest()
        answer = question.answers[0]
        self.assertTrue(answer)
        answer_data = {'question':question,
                       'description':'There are many ways to handle recursion',
                       'accepted':False,
                       'given_by':UserProfile.objects.latest()}
        Answer.objects.create_answer(question=answer_data['question'],
                                     description=answer_data['description'],
                                     accepted=answer_data['accepted'],
                                     userprofile=answer_data['given_by'])
        recent_answer = question.answers[0]
        self.assertTrue(recent_answer)
        self.assertNotEquals(answer.id, recent_answer.id)
    
    def test_accepting_an_answer(self):
        question = Question.objects.latest()
        answer = question.answers[0]
        answer.accept(accepted_by=question.raised_by)
        self.assertTrue(answer in question.answers)
        self.assertTrue(answer.accepted)
        self.assertEquals(answer.id, question.accepted_answer.id)
    
    def test_accepting_more_than_one_answer(self):
        question = Question.objects.latest()
        answer = question.answers[0]
        answer.accept(accepted_by=question.raised_by)
        self.assertTrue(answer.accepted)
        answer_data = {'question':question,
                       'description':'There are many ways to handle recursion',
                       'accepted':True,
                       'given_by':UserProfile.objects.latest()}
        Answer.objects.create_answer(question=answer_data['question'],
                                     description=answer_data['description'],
                                     accepted=answer_data['accepted'],
                                     userprofile=answer_data['given_by'])
        recent_answer = Answer.objects.latest()
        self.assertTrue(answer in question.answers)
        self.assertNotEquals(answer.id, recent_answer.id)
        self.assertTrue(recent_answer.accepted)
        self.assertEquals(recent_answer.id, question.accepted_answer.id)
        self.assertFalse(Answer.objects.get(id=answer.id).accepted)
    
    def test_accepting_answer_by_nonowner_of_a_question(self):
        somerandom_userprofile = UserProfile.objects.get(id=2)
        question = Question.objects.get(id=2)
        answer_data = {'question':question,
                       'description':'There are many ways to handle recursion',
                       'accepted':False,
                       'given_by':somerandom_userprofile}
        Answer.objects.create_answer(question=answer_data['question'],
                                     description=answer_data['description'],
                                     accepted=answer_data['accepted'],
                                     userprofile=answer_data['given_by'])
        answer = Answer.objects.latest()
        self.assertRaises(AnswerCantBeAcceptedException,
                          answer.accept,
                          accepted_by=answer_data['given_by'])
        self.assertFalse(answer.accepted)
        answer.accept(accepted_by=UserProfile.objects.get(id=1))
        self.assertTrue(answer.accepted)
    
    def test_unaccepting_an_answer(self):
        answer = Answer.objects.filter(accepted=True)[0]
        self.assertTrue(answer.accepted)
        answer.unaccept()
        answer = Answer.objects.get(id=answer.id)
        self.assertFalse(answer.accepted)
    
    def test_retrieving_all_answers_for_a_question(self):
        question = Question.objects.get(id=2)
        all_answers = question.answers
        for answer in all_answers:
            self.assertEquals(answer.question.id, question.id)
    
    def test_answering_a_closed_question(self):
        question = Question.objects.get(id=2)
        self.assertFalse(question.closed)
        question.close_answering()
        self.assertTrue(question.closed)
        answer_data = {'question':question,
                       'description':'There are many ways to handle recursion',
                       'accepted':False,
                       'given_by':UserProfile.objects.get(id=2)}
        self.assertRaises(AnsweringIsClosedException,
                          Answer.objects.create_answer,
                          question=answer_data['question'],
                          description=answer_data['description'],
                          accepted=answer_data['accepted'],
                          userprofile=answer_data['given_by'])