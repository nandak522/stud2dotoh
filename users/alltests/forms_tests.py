from utils import TestCase
from users.forms import UserSignupForm, UserLoginForm

class UserSignupFormTests(TestCase):
    fixtures = ['users.json']
    
    def test_valid_signup(self):
        data = {'username':'nanda.kishore',
                'password':'somevalidpasssword',
                'email':'nandakishore@gmail.com'}
        form = UserSignupForm(data)
        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)
        self.assertTrue(form.cleaned_data)
        
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
        self.assertEquals(form.errors.get('username')[0], 'Invalid Username!')
        self.assertFalse(form.errors.has_key('password'))