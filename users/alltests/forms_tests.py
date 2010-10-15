from utils import TestCase
from users.forms import UserSignupForm

class UserSignupFormTests(TestCase):
    
    def test_valid_signup(self):
        data = {'username':'nanda.kishore',
                'password':'somevalidpasssword',
                'email':'nandakishore@gmail.com'}
        form = UserSignupForm(data)
        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)
        self.assertTrue(form.cleaned_data) 
    