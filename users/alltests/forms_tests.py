from utils import TestCase
from users.forms import UserSignupForm, UserLoginForm, SaveFileForm, AccountSettingsForm
from django.conf import settings

class UserSignupFormTests(TestCase):
    fixtures = ['users.json']
    
    def test_valid_signup(self):
        data = {'name':'Nanda Kishore',
                'password':'somevalidpasssword',
                'email':'nandakishore@gmail.com'}
        form = UserSignupForm(data)
        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)
        self.assertTrue(hasattr(form, 'cleaned_data'))
        
    def test_duplicate_signup(self):
        data = {'name':'Nanda Kishore',
                'password':'nopassword',
                'email':'madhav.bnk@gmail.com'}
        form = UserSignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.has_key('email'))
        self.assertFalse(hasattr(form, 'cleaned_data'))
        
    def test_invalid_signup(self):
        data = {'name':'',
                'password':'',
                'email':''}
        form = UserSignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.has_key('name'))
        self.assertTrue(form.errors.has_key('email'))
        self.assertTrue(form.errors.has_key('password'))
        
class UserLoginFormTests(TestCase):
    fixtures = ['users.json']
    
    def test_valid_login(self):
        data = {'email':'madhav.bnk@gmail.com',
                'password':'nopassword'}
        form = UserLoginForm(data)
        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)
        
    def test_invalid_login(self):
        login_credentials = [{'email':'', 'password':''},
                             {'email':'madhavbnk', 'password':''},
                             {'email':'', 'password':'nopassword'},
                             {'email':'nonexistant_emailaddres', 'password':'somepassword'}]
        form = UserLoginForm(login_credentials[0])
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.has_key('email'))
        self.assertTrue(form.errors.has_key('password'))
        form = UserLoginForm(login_credentials[1])
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.has_key('email'))
        self.assertTrue(form.errors.has_key('password'))
        form = UserLoginForm(login_credentials[2])
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.has_key('email'))
        form = UserLoginForm(login_credentials[3])
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.has_key('email'))
        self.assertEquals(form.errors.get('email')[0], 'Enter a valid e-mail address.')
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
        
class AccountSettingsFormTests(TestCase):
    def test_empty_form_submission(self):
        data = {'name':'', 'slug':'', 'new_password':''}
        form = AccountSettingsForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.has_key('name'))
        self.assertFalse(form.errors.has_key('slug'))
        self.assertFalse(form.errors.has_key('new_password'))
    
    def test_invalid_name_submission(self):
        invalid_names = ['', '    ', '*(*(*(*']
        for name in invalid_names:
            form = AccountSettingsForm({'name':name, 'slug':'somedomain', 'new_password':'asdasdf'})
            self.assertFalse(form.is_valid())
            self.assertTrue(form.errors)
            self.assertTrue(form.errors.has_key('name'))
            self.assertFalse(form.errors.has_key('slug'))
            self.assertFalse(form.errors.has_key('new_password'))
    
    def test_valid_account_details_updation(self):
        data = {'name':'Nanda Kishore.B', 'slug':'madhavbnk', 'new_password':'somepass'}
        form = AccountSettingsForm(data)
        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)