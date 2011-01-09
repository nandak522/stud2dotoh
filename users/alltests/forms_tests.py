from utils import TestCase
from users.forms import StudentSignupForm, ProfessorSignupForm, EmployeeSignupForm
from users.forms import UserLoginForm, SaveNoteForm
from users.forms import PersonalSettingsForm, AcadSettingsForm, WorkInfoSettingsForm
from django.conf import settings

class StudentSignupFormTests(TestCase):
    fixtures = ['users.json']
    
    def test_valid_signup(self):
        data = {'name':'Nanda Kishore',
                'password':'somevalidpasssword',
                'email':'nandakishore@gmail.com',
                'college':'MGIT.'}
        form = StudentSignupForm(data)
        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)
        self.assertTrue(hasattr(form, 'cleaned_data'))
        
    def test_duplicate_signup(self):
        data = {'name':'Nanda Kishore',
                'password':'nopassword',
                'email':'madhav.bnk@gmail.com',
                'college':'MGIT.'}
        form = StudentSignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.has_key('email'))
        self.assertFalse(hasattr(form, 'cleaned_data'))
        
    def test_invalid_signup(self):
        data = {'name':'',
                'password':'',
                'email':'',
                'college':''}
        form = StudentSignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.has_key('name'))
        self.assertTrue(form.errors.has_key('email'))
        self.assertTrue(form.errors.has_key('password'))
        self.assertTrue(form.errors.has_key('college'))

class ProfessorSignupFormTests(TestCase):
    fixtures = ['users.json']
    
    def test_valid_signup(self):
        data = {'name':'Nanda Kishore',
                'password':'somevalidpasssword',
                'email':'nandakishore@gmail.com',
                'college':'MGIT.'}
        form = ProfessorSignupForm(data)
        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)
        self.assertTrue(hasattr(form, 'cleaned_data'))
        
    def test_duplicate_signup(self):
        #Same as Student Duplicate Signup
        pass
    
    def test_invalid_signup(self):
        #Same as Student Invalid Signup
        pass

class EmployeeSignupFormTests(TestCase):
    fixtures = ['users.json']
    
    def test_valid_signup(self):
        data = {'name':'Nanda Kishore',
                'password':'somevalidpasssword',
                'email':'nandakishore@gmail.com',
                'company':'MGIT.'}
        form = EmployeeSignupForm(data)
        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)
        self.assertTrue(hasattr(form, 'cleaned_data'))
        
    def test_duplicate_signup(self):
        data = {'name':'Nanda Kishore',
                'password':'nopassword',
                'email':'madhav.bnk@gmail.com',
                'company':'Infosys'}
        form = EmployeeSignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.has_key('email'))
        self.assertFalse(hasattr(form, 'cleaned_data'))
        
    def test_invalid_signup(self):
        data = {'name':'',
                'password':'',
                'email':'',
                'company':''}
        form = EmployeeSignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.has_key('name'))
        self.assertTrue(form.errors.has_key('email'))
        self.assertTrue(form.errors.has_key('password'))
        self.assertTrue(form.errors.has_key('company'))
     
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
        
class SaveNotepadFormTests(TestCase):
    def test_empty_form_submission(self):
        data = {'name':'','short_description':'','content':'', 'public':''}
        form = SaveNoteForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.has_key('name'))
        self.assertFalse(form.errors.has_key('short_description'))
        self.assertTrue(form.errors.has_key('content'))
        self.assertFalse(form.errors.has_key('public'))
        
    def test_empty_content_submission(self):
        data = {'name':'My C Assignment','short_description':'','content':'', 'public':True}
        form = SaveNoteForm(data)
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
        form = SaveNoteForm(data)
        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)
        self.assertEquals(data['content'].strip(), form.cleaned_data.get('content'))
        
class PersonalSettingsFormTests(TestCase):
    def test_empty_form_submission(self):
        data = {'name':'', 'slug':'', 'new_password':''}
        form = PersonalSettingsForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.has_key('name'))
        self.assertFalse(form.errors.has_key('slug'))
        self.assertFalse(form.errors.has_key('new_password'))
    
    def test_invalid_name_submission(self):
        invalid_names = ['', '    ', '*(*(*(*']
        for name in invalid_names:
            form = PersonalSettingsForm({'name':name, 'slug':'somedomain', 'new_password':'asdasdf'})
            self.assertFalse(form.is_valid())
            self.assertTrue(form.errors)
            self.assertTrue(form.errors.has_key('name'))
            self.assertFalse(form.errors.has_key('slug'))
            self.assertFalse(form.errors.has_key('new_password'))
    
    def test_valid_account_details_updation(self):
        data = {'name':'Nanda Kishore.B', 'slug':'madhavbnk', 'new_password':'somepass'}
        form = PersonalSettingsForm(data)
        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)
        
class AcadSettingsFormTests(TestCase):
    def test_direct_empty_form_submission(self):
        data = {'branch':'CSE', 'college':'', 'start_year':'2011', 'end_year':'2015'}
        form = AcadSettingsForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors.has_key('college'))
    
    def test_invalid_academic_details_submission(self):
        datas = [{'branch':'CSE', 'college':'*(*(*(*(', 'start_year':'2011', 'end_year':'2015'},
                 {'branch':'CSE', 'college':'JNTU, Hyderabad', 'start_year':'2011', 'end_year':'2015'}]
        for data in datas:
            form = AcadSettingsForm(data)
            self.assertFalse(form.is_valid())
            self.assertTrue(form.errors.has_key('college'))
    
    def test_valid_academic_details_saving(self):
        datas = [{'branch':'CSE', 'college':'SVPCET', 'start_year':'2011', 'end_year':'2015'},
                 {'branch':'CSE', 'college':'Sri Venkatesa Perumal College of Engineering and Technology', 'start_year':'2001', 'end_year':'2005'},
                 {'branch':'CSE', 'college':'MGIT.', 'start_year':'2011', 'end_year':'2015'},
                 {'branch':'CSE', 'college':'Mohan-Babu College-Chittor.', 'start_year':'1930', 'end_year':'2015'}]
        for data in datas:
            form = AcadSettingsForm(data)
            self.assertTrue(form.is_valid())
            self.assertFalse(form.errors)
            for key,val in data.items():
                self.assertEquals(data[key], form.cleaned_data.get(key))
    
class WorkInfoSettingsFormTests(TestCase):
    def test_empty_form_submission(self):
        data = {'workplace':'', 'designation':'', 'years_of_exp':''}
        form = WorkInfoSettingsForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
    
    def test_valid_form_submission(self):
        datas = [{'workplace':'Sri Venkatesa Perumal College of Engineering & Technology.', 'designation':'Computer Science Professor', 'years_of_exp':'2'},
                 {'workplace':'Infosys', 'designation':'Software Architect', 'years_of_exp':'4'},
                 {'workplace':'IBM Global-Services', 'designation':'IT Guy-Bangalore', 'years_of_exp':'1.5'}]
        for data in datas:
            form = WorkInfoSettingsForm(data)
            self.assertTrue(form.is_valid())
            self.assertFalse(form.errors)
    
    def test_invalid_form_submission(self):
        invalid_workplace_names = ('()(**&*&', '%$%$%$%')
        datas = [{'workplace':invalid_workplace_names[0], 'designation':'Computer Science Professor', 'years_of_exp':'2'},
                 {'workplace':invalid_workplace_names[1], 'designation':'Software Architect', 'years_of_exp':'1.5'}]
        for data in datas:
            form = WorkInfoSettingsForm(data)
            self.assertFalse(form.is_valid())
            self.assertTrue(form.errors)
            self.assertTrue(form.errors.has_key('workplace'))
            self.assertFalse(form.errors.has_key('designation'))
            self.assertFalse(form.errors.has_key('years_of_exp'))