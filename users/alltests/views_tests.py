from utils import TestCase
from django.conf import settings
from django.core.urlresolvers import reverse as url_reverse
from users.models import UserProfile

class MainSignupPageTests(TestCase):
    def test_fresh_anonymous_access(self):
        raise NotImplementedError
    
    def test_fresh_authenticated_access(self):
        raise NotImplementedError

class StudentSignupTests(TestCase):
    fixtures = ['users.json']
    
    def test_valid_signup(self):
        form_data = {'email': 'someuser@gmail.com',
                     'password': 'abc123',
                     'name': 'somename',
                     'college':'CBIT, Hyderabad.'}
        response = self.client.post(path='/accounts/studentregister/',#TODO:url hardcoding is bad.
                                    data=form_data)
        self.assertRedirects(response,
                             expected_url=url_reverse('users.views.view_homepage'),
                             status_code=302,
                             target_status_code=200)
        response = self.client.get(path=url_reverse('users.views.view_homepage'))
        self.assertTemplateUsed(response, 'dashboard.html')
        context = response.context[0]
        self.assertTrue(context.has_key('userprofile'))
        userprofile = context.get('userprofile')
        self.assertTrue(userprofile)
        self.assertEquals(userprofile.user.email, form_data['email'])
        self.assertTrue(userprofile.check_password(form_data['password']))
        self.assertTrue(context.has_key('userprofilegroup'))
        userprofilegroup = context.get('userprofilegroup')
        self.assertEquals(userprofilegroup, 'Student')
        
    def test_invalid_signup(self):
        form_data = {'email': '',
                     'password': '',
                     'name': '',
                     'college': ''}
        response = self.client.post(path='/accounts/studentregister/',#TODO:url hardcoding is bad.
                                    data=form_data)
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_register.html')
        context = response.context[0]
        form = context.get('form')
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.get('email'))
        self.assertTrue(form.errors.get('password'))
        self.assertTrue(form.errors.get('name'))
        self.assertFalse(context.has_key('userprofile'))
        self.assertFalse(context.has_key('userprofilegroup'))
    
    def test_duplicate_signup(self):
        form_data = {'email': 'madhav.bnk@gmail.com',
                     'password': 'somepassword',
                     'name': 'NandaKishore',
                     'college': 'SomeOtherCollege'}
        response = self.client.post(path='/accounts/studentregister/',#TODO:url hardcoding is bad.
                                    data=form_data)
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_register.html')
        context = response.context[0]
        form = context.get('form')
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.get('email'))
        self.assertFalse(context.has_key('userprofile'))
        self.assertFalse(context.has_key('userprofilegroup'))
        
class ProfessorSignupTests(TestCase):
    fixtures = ['users.json']
    
    def test_valid_signup(self):
        form_data = {'email': 'someprof@gmail.com',
                     'password': 'abc123',
                     'name': 'someprof',
                     'college':'CBIT, Hyderabad.'}
        response = self.client.post(path='/accounts/professorregister/',#TODO:url hardcoding is bad.
                                    data=form_data)
        self.assertRedirects(response,
                             expected_url=url_reverse('users.views.view_homepage'),
                             status_code=302,
                             target_status_code=200)
        response = self.client.get(path=url_reverse('users.views.view_homepage'))
        self.assertTemplateUsed(response, 'dashboard.html')
        context = response.context[0]
        self.assertTrue(context.has_key('userprofile'))
        userprofile = context.get('userprofile')
        self.assertTrue(userprofile)
        self.assertEquals(userprofile.user.email, form_data['email'])
        self.assertTrue(userprofile.check_password(form_data['password']))
        self.assertTrue(context.has_key('userprofilegroup'))
        userprofilegroup = context.get('userprofilegroup')
        self.assertEquals(userprofilegroup, 'Professor')
        
    def test_invalid_signup(self):
        form_data = {'email': '',
                     'password': '',
                     'name': '',
                     'college': ''}
        response = self.client.post(path='/accounts/professorregister/',#TODO:url hardcoding is bad.
                                    data=form_data)
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'professor_register.html')
        context = response.context[0]
        form = context.get('form')
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.get('email'))
        self.assertTrue(form.errors.get('password'))
        self.assertTrue(form.errors.get('name'))
        self.assertFalse(context.has_key('userprofile'))
        self.assertFalse(context.has_key('userprofilegroup'))
    
    def test_duplicate_signup(self):
        form_data = {'email': 'madhav.bnk@gmail.com',
                     'password': 'somepassword',
                     'name': 'NandaKishore',
                     'college': 'SomeOtherCollege'}
        response = self.client.post(path='/accounts/professorregister/',#TODO:url hardcoding is bad.
                                    data=form_data)
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'professor_register.html')
        context = response.context[0]
        form = context.get('form')
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.get('email'))
        self.assertFalse(context.has_key('userprofile'))
        self.assertFalse(context.has_key('userprofilegroup'))
        
class EmployeeSignupTests(TestCase):
    fixtures = ['users.json']
    
    def test_valid_signup(self):
        form_data = {'email': 'someemployee@gmail.com',
                     'password': 'abc123',
                     'name': 'someemployee',
                     'company':'Infosys'}
        response = self.client.post(path='/accounts/employeeregister/',#TODO:url hardcoding is bad.
                                    data=form_data)
        self.assertRedirects(response,
                             expected_url=url_reverse('users.views.view_homepage'),
                             status_code=302,
                             target_status_code=200)
        response = self.client.get(path=url_reverse('users.views.view_homepage'))
        self.assertTemplateUsed(response, 'dashboard.html')
        context = response.context[0]
        self.assertTrue(context.has_key('userprofile'))
        userprofile = context.get('userprofile')
        self.assertTrue(userprofile)
        self.assertEquals(userprofile.user.email, form_data['email'])
        self.assertTrue(userprofile.check_password(form_data['password']))
        self.assertTrue(context.has_key('userprofilegroup'))
        userprofilegroup = context.get('userprofilegroup')
        self.assertEquals(userprofilegroup, 'Employee')
        
    def test_invalid_signup(self):
        form_data = {'email': '',
                     'password': '',
                     'name': '',
                     'company': ''}
        response = self.client.post(path='/accounts/employeeregister/',#TODO:url hardcoding is bad.
                                    data=form_data)
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee_register.html')
        context = response.context[0]
        form = context.get('form')
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.get('email'))
        self.assertTrue(form.errors.get('password'))
        self.assertTrue(form.errors.get('name'))
        self.assertFalse(context.has_key('userprofile'))
        self.assertFalse(context.has_key('userprofilegroup'))
    
    def test_duplicate_signup(self):
        form_data = {'email': 'madhav.bnk@gmail.com',
                     'password': 'somepassword',
                     'name': 'NandaKishore',
                     'company': 'SomeOtherCollege'}
        response = self.client.post(path='/accounts/employeeregister/',#TODO:url hardcoding is bad.
                                    data=form_data)
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee_register.html')
        context = response.context[0]
        form = context.get('form')
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.get('email'))
        self.assertFalse(context.has_key('userprofile'))
        self.assertFalse(context.has_key('userprofilegroup'))

class UserLoginTests(TestCase):
    fixtures = ['users.json']
    
    def test_valid_userlogin(self):
        form_data = {'email': 'madhav.bnk@gmail.com',
                     'password': 'nopassword'}
        response = self.client.post(path=url_reverse('users.views.view_login'),
                                    data=form_data)
        self.assertRedirects(response,
                             expected_url=url_reverse('users.views.view_homepage'),
                             status_code=302,
                             target_status_code=200)
        response = self.client.get(url_reverse('users.views.view_homepage'))
        self.assertEquals(response.context[0].get('user').email, form_data['email'])
        
    def test_invalid_userlogin(self):
        for email in ('invalidemailformat', '&*&*&*67688'):
            response = self.client.post(path=url_reverse('users.views.view_login'),
                                        data={'email': email, 'password': 'abc123'})
            self.assertTrue(response)
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, 'login.html')
            context = response.context[0]
            form = context.get('form')
            self.assertTrue(form.errors)
            self.assertTrue(form.errors.get('email'))
            
class UserLogoutTests(TestCase):
    fixtures = ['users.json']
    
    def test_logout_link_visibility(self):
        response = self.client.get(path=url_reverse('users.views.view_homepage'))
        self.assertTrue('Logout' not in response.content)
        self.login_as(email='madhav.bnk@gmail.com', password='nopassword')
        response = self.client.get(path=url_reverse('users.views.view_homepage'))
        self.assertTrue('Logout' in response.content)
    
    def test_anonymous_user_logout(self):
        response = self.client.get(path=url_reverse('users.views.view_logout'))
        self.assertRedirects(response,
                             expected_url=url_reverse('users.views.view_homepage'),
                             status_code=302,
                             target_status_code=200)
        #TODO:Need to validate the confirmation message for logout
    
    def test_authenticated_user_logout(self):
        self.login_as(email='madhav.bnk@gmail.com', password='nopassword')
        response = self.client.get(path=url_reverse('users.views.view_logout'))
        self.assertRedirects(response,
                             expected_url=url_reverse('users.views.view_homepage'),
                             status_code=302,
                             target_status_code=200)
        response = self.client.get(path=url_reverse('users.views.view_notepad'))
        self.assertRedirects(response,
                             expected_url='/accounts/login/?next=/notepad/',
                             status_code=302,
                             target_status_code=200)
            
class UserProfilePageTests(TestCase):
    fixtures = ['users.json']
    
    def test_userprofilepage_success_response(self):
        userprofile = UserProfile.objects.get(user__email='somerandomuser@gmail.com')
        response = self.client.get(path=url_reverse('users.views.view_userprofile', args=(userprofile.slug,)))
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_profile.html')
        context = response.context[0]
        self.assertTrue(context.has_key('userprofile'))
        userprofile = context.get('userprofile')
        self.assertEquals(userprofile.user.email, UserProfile.objects.get(user__email='somerandomuser@gmail.com').user.email)
        self.assertTrue(context.has_key('all_notes'))
        self.login_as(email='somerandomuser@gmail.com', password='nopassword')
        form_data = {'name': 'My Python Assignment',
                     'short_description': 'Hello World',
                     'content': 'print "Hello World"',
                     'public': True}
        response = self.client.post(path=url_reverse('users.views.view_notepad'),
                                    data=form_data)
        self.logout()
        response = self.client.get(path=url_reverse('users.views.view_userprofile', args=(userprofile.slug,)))
        context = response.context[0]
        all_notes = context.get('all_notes')
        self.assertTrue(all_notes)
        from utils import slugify
        self.assertTrue(slugify(form_data['name']) in all_notes)
        self.assertTrue(context.has_key('asked_questions'))
        self.assertTrue(context.has_key('answered_questions'))
    
    def test_invalidlink_for_userprofilepage(self):
        userprofile = UserProfile.objects.get(user__email='madhav.bnk@gmail.com')
        response = self.client.get(path=url_reverse('users.views.view_userprofile', args=('madness',)))
        self.assertTrue(response)
        self.assertEquals(response.status_code, 404)

class UserNotepadSavingTests(TestCase):
    fixtures = ['users.json']
    
    def test_access_to_notepad_page(self):
        response = self.client.get(path=url_reverse('users.views.view_notepad'))
        self.assertRedirects(response,
                             expected_url='/accounts/login/?next=/notepad/',
                             status_code=302,
                             target_status_code=200)        
        self.login_as(email='madhav.bnk@gmail.com', password='nopassword')
        response = self.client.get(path=url_reverse('users.views.view_notepad'))
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'notepad.html')
        context = response.context[0]
        form = context.get('form')
        self.assertFalse(form.is_bound)
        self.assertFalse(form.errors)
        self.assertTrue(context.has_key('all_notes'))

    def test_empty_notepad_saving(self):
        self.login_as(email='madhav.bnk@gmail.com', password='nopassword')
        form_data = {'name': '',
                     'short_description': '',
                     'content': '',
                     'public': True}
        response = self.client.post(path=url_reverse('users.views.view_notepad'),
                                    data=form_data)
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'notepad.html')
        context = response.context[0]
        self.assertTrue(context.has_key('form'))
        form = context.get('form')
        self.assertTrue(form.is_bound)
        self.assertTrue(form.errors)
        self.assertTrue(context.has_key('all_notes'))
        all_notes = context.get('all_notes')
        self.assertFalse(all_notes)
    
    def test_valid_notepad_saving(self):
        self.login_as(email='madhav.bnk@gmail.com', password='nopassword')
        form_data = {'name': 'My Python Assignment',
                     'short_description': 'Hello World',
                     'content': 'print "Hello World"',
                     'public': True}
        response = self.client.post(path=url_reverse('users.views.view_notepad'),
                                    data=form_data)
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'notepad.html')
        context = response.context[0]
        self.assertTrue(context.has_key('form'))
        form = context.get('form')
        self.assertFalse(form.is_bound)
        self.assertFalse(form.errors)
        self.assertTrue(context.has_key('all_notes'))
        all_notes = context.get('all_notes')
        self.assertTrue(all_notes)
        from utils import slugify
        self.assertTrue(slugify(form_data['name']) in all_notes)
        
    def test_viewing_saved_notepad_content(self):
        self.login_as(email='madhav.bnk@gmail.com', password='nopassword')
        data = {'name':'My last semister Assignment',
                'short_description':'',
                'content':open("/".join([settings.ROOT_PATH, 'users', 'fixtures', 'assignment.py'])).read(),
                'public':True}
        response = self.client.post(path=url_reverse('users.views.view_notepad'),
                                    data=data)
        self.assertTrue(response)
        from utils import slugify
        response = self.client.get(url_reverse('users.views.view_file_content_view', args=(slugify(data['name']),)))
        self.assertTrue(response)
        self.assertEquals(response['Content-Type'], 'text/plain')
        self.assertEquals(response.content, data['content'])
        
    def test_viewing_invalid_notepad_file_content(self):
        self.login_as(email='madhav.bnk@gmail.com', password='nopassword')
        data = {'name':'some_non_existing_filename'}
        from utils import slugify 
        response = self.client.get(url_reverse('users.views.view_file_content_view', args=(slugify(data['name']),)))
        self.assertTrue(response)
        self.assertEquals(response.status_code, 404)
        
class AccountSettingsPageTests(TestCase):
    fixtures = ['users.json', 'colleges.json', 'acadinfo.json']
    
    def test_settings_page_access_anonymously(self):
        response = self.client.get(url_reverse('users.views.view_account_settings'))
        self.assertRedirects(response,
                             expected_url='/accounts/login/?next=/settings/',
                             status_code=302,
                             target_status_code=200)
        
    def test_fresh_settings_page_access_by_student(self):
        self.login_as(email='somerandomuser@gmail.com', password='nopassword')
        response = self.client.get(url_reverse('users.views.view_account_settings'))
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'personal_settings.html')
        context = response.context[0]
        self.assertTrue(context.has_key('personal_form'))
        form = context.get('personal_form')
        self.assertFalse(form.errors)
        self.assertTemplateUsed(response, 'acad_settings.html')
        self.assertTrue(context.has_key('acad_form'))
        form = context.get('acad_form')
        self.assertFalse(form.errors)
        self.assertFalse(context.has_key('workinfo_form'))
    
    def test_fresh_settings_page_access_by_professor(self):
        self.login_as(email='someprof@gmail.com', password='nopassword')
        response = self.client.get(url_reverse('users.views.view_account_settings'))
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'personal_settings.html')
        context = response.context[0]
        self.assertTrue(context.has_key('personal_form'))
        form = context.get('personal_form')
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.get('slug'))
        self.assertFalse(form.errors.get('name'))
        self.assertFalse(form.errors.get('new_password'))
        self.assertTemplateUsed(response, 'acad_settings.html')
        self.assertTrue(context.has_key('acad_form'))
        form = context.get('acad_form')
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.get('branch'))
        self.assertTrue(form.errors.get('college'))
        self.assertFalse(form.errors.get('start_year'))
        self.assertFalse(form.errors.get('end_year'))
        self.assertTrue(context.has_key('workinfo_form'))
        form = context.get('workinfo_form')
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.get('workplace'))
        self.assertFalse(form.errors.get('designation'))
        self.assertTrue(form.errors.get('years_of_exp'))
    
    def test_fresh_settings_page_access_by_employee(self):
        self.login_as(email='someemployee@gmail.com', password='nopassword')
        response = self.client.get(url_reverse('users.views.view_account_settings'))
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'personal_settings.html')
        context = response.context[0]
        self.assertTrue(context.has_key('personal_form'))
        form = context.get('personal_form')
        self.assertFalse(form.errors)
        self.assertTemplateUsed(response, 'acad_settings.html')
        self.assertTrue(context.has_key('acad_form'))
        form = context.get('acad_form')
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.get('branch'))
        self.assertTrue(form.errors.get('college'))
        self.assertFalse(form.errors.get('start_year'))
        self.assertFalse(form.errors.get('end_year'))
        self.assertTrue(context.has_key('workinfo_form'))
        form = context.get('workinfo_form')
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.get('workplace'))
        self.assertFalse(form.errors.get('designation'))
        self.assertTrue(form.errors.get('years_of_exp'))
    
    def test_saving_personal_settings_by_student(self):
        self.login_as(email='madhav.bnk@gmail.com', password='nopassword')
        data = {'name':'Nanda.B',
                'new_password':'newpassword',
                'slug':'nandakishore'}
        response = self.client.post(path=url_reverse('users.views.view_save_personal_settings'),
                                    data=data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertTrue(response)
        context = response.context
        self.assertTrue(context.has_key('personal_form'))
        personal_form = context.get('personal_form')
        self.assertFalse(personal_form.errors)
        userprofile = context.get('userprofile')
        self.assertTrue(userprofile.check_password(data['new_password']))
        from django.contrib.sites.models import Site
        self.assertEqual(userprofile.domain, ".".join([userprofile.slug, Site.objects.get(id=settings.SITE_ID).domain]))
        self.assertEqual(userprofile.name, data['name'])
    
    def test_saving_academic_settings_by_student_and_professor(self):
        login_details = (('madhav.bnk@gmail.com', 'nopassword'), ('someprof@gmail.com', 'nopassword'))
        for login in login_details:
            self.login_as(email=login[0], password=login[1])
            data = {'branch':'CSE',
                    'college':'Vasavi College of Engg.',
                    'start_year':1998,
                    'end_year':1999}
            response = self.client.post(path=url_reverse('users.views.view_save_acad_settings'),
                                        data=data,
                                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            self.assertTrue(response)
            context = response.context
            self.assertTrue(context.has_key('acad_form'))
            acad_form = context.get('acad_form')
            self.assertFalse(acad_form.errors)
            userprofile = context.get('userprofile')
            acad_details = userprofile.acad_details
            self.assertEquals(acad_details[0], data['branch'])
            self.assertEquals(acad_details[1].name, data['college'])
            self.assertEquals(acad_details[2], data['start_year'])
            self.assertEquals(acad_details[3], data['end_year'])
            self.logout()
        
    def test_saving_workplace_settings_by_employee(self):
        self.login_as(email='someemployee@gmail.com', password='nopassword')
        data = {'workplace':'Infosys',
                'designation':'Software Architect',
                'years_of_exp':2.4}
        response = self.client.post(path=url_reverse('users.views.view_save_workinfo_settings'),
                                    data=data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertTrue(response)
        context = response.context
        self.assertTrue(context.has_key('workinfo_form'))
        workinfo_form = context.get('workinfo_form')
        self.assertFalse(workinfo_form.errors)
        userprofile = context.get('userprofile')
        work_details = userprofile.work_details
        self.assertEquals(work_details[0].name, data['workplace'])
        self.assertEquals(work_details[1], data['designation'])
        self.assertEquals(float(work_details[2]), data['years_of_exp'])
        self.logout()
    
    def test_saving_domain_url_once_and_twice(self):
        self.login_as(email='madhav.bnk@gmail.com', password='nopassword')
        response = self.client.get(path=url_reverse('users.views.view_account_settings'))
        context = response.context[0]
        self.assertTrue(context.has_key('personal_form'))
        personal_form = context.get('personal_form')
        self.assertTrue(personal_form.errors)
        data = {'name':'Nanda.B',
                'new_password':'newpassword',
                'slug':'nandakishore'}
        response = self.client.post(path=url_reverse('users.views.view_save_personal_settings'),
                                    data=data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertTrue(response)
        context = response.context
        self.assertTrue(context.has_key('personal_form'))
        personal_form = context.get('personal_form')
        self.assertFalse(personal_form.errors)
        userprofile = context.get('userprofile')
        self.assertTrue(userprofile.check_password(data['new_password']))
        from django.contrib.sites.models import Site
        self.assertEqual(userprofile.domain, ".".join([userprofile.slug, Site.objects.get(id=settings.SITE_ID).domain]))
        self.assertEqual(userprofile.name, data['name'])
        response = self.client.get(path=url_reverse('users.views.view_account_settings'))
        self.assertTrue(userprofile.domain in response.content)
        from users.models import CantUpdateSlugAgainException
        self.assertRaises(CantUpdateSlugAgainException,
                          userprofile.update_slug,
                          new_slug_name='newslug')