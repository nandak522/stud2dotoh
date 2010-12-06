from utils import TestCase
from django.conf import settings
from django.core.urlresolvers import reverse as url_reverse
from users.models import UserProfile

class UserSignupTests(TestCase):
    def test_valid_usersignup(self):
        form_data = {'email': 'someuser@gmail.com',
                     'password': 'abc123',
                     'name': 'somename'}
        response = self.client.post(path=url_reverse('users.views.view_register'),
                                    data=form_data)
        self.assertRedirects(response,
                             expected_url=url_reverse('users.views.view_homepage'),
                             status_code=302,
                             target_status_code=200)
        response = self.client.get(path=url_reverse('users.views.view_homepage'))
        self.assertTemplateUsed(response, 'dashboard.html')
        userprofile = UserProfile.objects.latest()
        self.assertTrue(userprofile)
        self.assertEquals(userprofile.user.email, form_data['email'])
        self.assertTrue(userprofile.check_password(form_data['password']))

    def test_invalid_usersignup(self):
        form_data = {'email': '',
                     'password': '',
                     'name': ''}
        response = self.client.post(path=url_reverse('users.views.view_register'),
                                    data=form_data)
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        context = response.context[0]
        form = context.get('form')
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.get('email'))
        self.assertTrue(form.errors.get('password'))
        self.assertTrue(form.errors.get('name'))

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
            
class UserProfilePageTests(TestCase):
    fixtures = ['users.json']
    
    def test_userprofilepage_success_response(self):
        userprofile = UserProfile.objects.get(user__email='somerandomuser@gmail.com')
        response = self.client.get(path=url_reverse('users.views.view_userprofile', args=(userprofile.id, userprofile.slug)))
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_profile.html')
        context = response.context[0]
        self.assertTrue(context.has_key('userprofile'))
        userprofile = context.get('userprofile')
        self.assertEquals(userprofile.user.email, UserProfile.objects.get(user__email='somerandomuser@gmail.com').user.email)
        self.assertTrue(context.has_key('public_uploaded_files'))
        self.login_as(email='somerandomuser', password='nopassword')
        form_data = {'name': 'My Python Assignment',
                     'short_description': 'Hello World',
                     'content': 'print "Hello World"',
                     'public': True}
        response = self.client.post(path=url_reverse('users.views.view_notepad'),
                                    data=form_data)
        self.logout()
        response = self.client.get(path=url_reverse('users.views.view_userprofile', args=(userprofile.id, userprofile.slug)))
        context = response.context[0]
        public_uploaded_files = context.get('public_uploaded_files')
        self.assertTrue(public_uploaded_files)
        from utils import slugify
        self.assertTrue(slugify(form_data['name']) in public_uploaded_files)
    
    def test_invalidlink_for_userprofilepage(self):
        userprofile = UserProfile.objects.get(user__email='madhav.bnk@gmail.com')
        response = self.client.get(path=url_reverse('users.views.view_userprofile', args=(userprofile.id, 'madness')))
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
        self.assertTrue(context.has_key('public_uploaded_files'))

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
        self.assertTrue(context.has_key('public_uploaded_files'))
        public_uploaded_files = context.get('public_uploaded_files')
        self.assertFalse(public_uploaded_files)
    
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
        self.assertTrue(context.has_key('public_uploaded_files'))
        public_uploaded_files = context.get('public_uploaded_files')
        self.assertTrue(public_uploaded_files)
        from utils import slugify
        self.assertTrue(slugify(form_data['name']) in public_uploaded_files)
        
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
        
class AccountSettingsTests(TestCase):
    fixtures = ['users.json']
    
    def test_valid_account_settings_form(self):
        raise NotImplementedError
    
    def test_saving_domain_url_first_time(self):
        raise NotImplementedError
    
    def test_saving_domain_url_from_second_time(self):
        raise NotImplementedError
    
    def test_empty_form_submission(self):
        raise NotImplementedError
    
    def test_invalid_form_submission(self):
        raise NotImplementedError