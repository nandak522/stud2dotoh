from utils import TestCase
from users.forms import UserSignupForm, UserLoginForm, SaveFileForm
from django.conf import settings

class UserSignupFormTests(TestCase):
    fixtures = ['users.json']
    
    def test_valid_signup(self):
        data = {'username':'nanda.kishore',
                'password':'somevalidpasssword',
                'email':'nandakishore@gmail.com'}
        form = UserSignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertFalse(hasattr(form, 'cleaned_data'))
        
    def test_duplicate_signup(self):
        data = {'username':'madhavbnk',
                'password':'nopassword',
                'email':'madhav.bnk@gmail.com'}
        form = UserSignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.has_key('email'))
        self.assertFalse(hasattr(form, 'cleaned_data'))
        
    def test_invalid_signup(self):
        data = {'username':'',
                'password':'',
                'email':''}
        form = UserSignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.has_key('username'))
        self.assertFalse(form.errors.has_key('email'))
        self.assertTrue(form.errors.has_key('password'))
        
class UserLoginFormTests(TestCase):
    fixtures = ['users.json']
    
    def test_valid_login(self):
        data = {'username':'madhavbnk',
                'password':'nopassword'}
        form = UserLoginForm(data)
        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)
        
    def test_invalid_login(self):
        login_credentials = [{'username':'', 'password':''},
                             {'username':'madhavbnk', 'password':''},
                             {'username':'', 'password':'nopassword'},
                             {'username':'nonexistant_username', 'password':'somepassword'}]
        form = UserLoginForm(login_credentials[0])
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.has_key('username'))
        self.assertTrue(form.errors.has_key('password'))
        form = UserLoginForm(login_credentials[1])
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertFalse(form.errors.has_key('username'))
        self.assertTrue(form.errors.has_key('password'))
        form = UserLoginForm(login_credentials[2])
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.has_key('username'))
        form = UserLoginForm(login_credentials[3])
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.has_key('username'))
        self.assertEquals(form.errors.get('username')[0], 'Invalid Username! Username should only be alphabetic. a-z,A-Z,0-9')
        self.assertFalse(form.errors.has_key('password'))
        
class SaveFileFormTests(TestCase):
    def test_empty_form_submission(self):
        data = {'name':'','short_description':'','content':'', 'public':''}
        form = SaveFileForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.has_key('name'))
        self.assertFalse(form.errors.has_key('short_description'))
        self.assertTrue(form.errors.has_key('content'))
        self.assertFalse(form.errors.has_key('public'))
        
    def test_empty_content_submission(self):
        data = {'name':'My C Assignment','short_description':'','content':'', 'public':True}
        form = SaveFileForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertFalse(form.errors.has_key('name'))
        self.assertFalse(form.errors.has_key('short_description'))
        self.assertTrue(form.errors.has_key('content'))
        self.assertFalse(form.errors.has_key('public'))
        
    def test_valid_form_submission(self):
        data = {'name':'My last semister Assignment',
                'short_description':'',
                'content':open("/".join([settings.ROOT_PATH, 'users', 'fixtures', 'assignment.py'])).read(),
                'public':True}
        form = SaveFileForm(data)
        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)
        self.assertEquals(data['content'].strip(), form.cleaned_data.get('content'))