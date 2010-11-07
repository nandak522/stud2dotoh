from utils import TestCase
from django.conf import settings
from django.core.urlresolvers import reverse as url_reverse
from users.models import UserProfile

class UserSignupTests(TestCase):
    def test_valid_usersignup(self):
        form_data = {'username': 'someuser',
                     'password': 'abc123',
                     'name': 'somename',
                     'email': 'someuser@gmail.com'}
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
        self.assertEquals(userprofile.user.username, form_data['username'])
        self.assertEquals(userprofile.user.email, form_data['email'])

    def test_invalid_usersignup(self):
        form_data = {'username': '',
                     'password': '',
                     'name': '',
                     'email': ''}
        response = self.client.post(path=url_reverse('users.views.view_register'),
                                    data=form_data)
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        context = response.context[0]
        form = context.get('form')
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertTrue(form.errors.get('username'))
        self.assertTrue(form.errors.get('password'))
        self.assertFalse(form.errors.get('name'))
        self.assertFalse(form.errors.get('email'))

class UserLoginTests(TestCase):
    fixtures = ['users.json']
    
    def test_valid_userlogin(self):
        form_data = {'username': 'madhavbnk',
                     'password': 'nopassword'}
        response = self.client.post(path=url_reverse('users.views.view_login'),
                                    data=form_data)
        self.assertRedirects(response,
                             expected_url=url_reverse('users.views.view_homepage'),
                             status_code=302,
                             target_status_code=200)
        response = self.client.get(url_reverse('users.views.view_homepage'))
        self.assertEquals(response.context[0].get('user').username, form_data['username'])
        
    def test_invalid_userlogin(self):
        for username in ('invalidusername', '&*&*&*67688'):
            response = self.client.post(path=url_reverse('users.views.view_login'),
                                        data={'username': username, 'password': 'abc123'})
            self.assertTrue(response)
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, 'login.html')
            context = response.context[0]
            form = context.get('form')
            self.assertTrue(form.errors)
            self.assertTrue(form.errors.get('username'))
            
#class UserProfilePageTests(TestCase):
#    fixtures = ['users.json']
#    
#    def test_userprofilepage_success_response(self):
#        userprofile = UserProfile.objects.get(email='madhav.bnk@gmail.com')
#        response = self.client.get(path=url_reverse('users.views.view_userprofile', args=(userprofile.id, userprofile.slug)))
#        self.assertTrue(response)
#        self.assertEquals(response.status_code, 200)
#        self.assertTemplateUsed(response, 'user_profile.html')
#        context = response.context[0]
#        self.assertTrue(context.has_key('userprofile'))
#        userprofile = context.get('userprofile')
#        self.assertEquals(userprofile, UserProfile.objects.get(email='madhav.bnk@gmail.com'))
#        self.assertTrue(context.has_key('submitted_snippets'))
#        submitted_snippets = context.get('submitted_snippets')
#        from quest.models import Snippet
#        snippet = Snippet.objects.get(slug=submitted_snippets[0]['slug'])
#        snippet_submitter = snippet.userprofilesnippetmembership_set.all()[0]
#        self.assertEquals(userprofile, snippet_submitter.userprofile)
#    
#    def test_invalidlink_for_userprofilepage(self):
#        userprofile = UserProfile.objects.get(email='madhav.bnk@gmail.com')
#        response = self.client.get(path=url_reverse('users.views.view_userprofile', args=(userprofile.id, 'madness')))
#        self.assertTrue(response)
#        self.assertEquals(response.status_code, 404)

class UserUploadFilesTests(TestCase):
    fixtures = ['users.json']
    
    def test_access_to_notepad_page(self):
        response = self.client.get(path=url_reverse('users.views.view_notepad'))
        self.assertRedirects(response,
                             expected_url='/accounts/login/?next=/notepad/',
                             status_code=302,
                             target_status_code=200)        
        self.login_as(username='madhavbnk', password='nopassword')
        response = self.client.get(path=url_reverse('users.views.view_notepad'))
        self.assertTrue(response)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'notepad.html')
        context = response.context[0]
        form = context.get('form')
        self.assertFalse(form.is_bound)
        self.assertFalse(form.errors)
        self.assertTrue(context.has_key('all_uploaded_files'))

    def test_empty_notepad_saving(self):
        self.login_as(username='madhavbnk', password='nopassword')
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
        self.assertTrue(context.has_key('all_uploaded_files'))
        all_uploaded_files = context.get('all_uploaded_files')
        self.assertFalse(all_uploaded_files)
    
    def test_valid_notepad_saving(self):
        self.login_as(username='madhavbnk', password='nopassword')
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
        self.assertTrue(context.has_key('all_uploaded_files'))
        all_uploaded_files = context.get('all_uploaded_files')
        self.assertTrue(all_uploaded_files)
        from utils import slugify
        self.assertTrue(slugify(form_data['name']) in all_uploaded_files)
        
    def test_viewing_saved_notepad_content(self):
        self.login_as(username='madhavbnk', password='nopassword')
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
        self.login_as(username='madhavbnk', password='nopassword')
        data = {'name':'some_non_existing_filename'}
        from utils import slugify 
        response = self.client.get(url_reverse('users.views.view_file_content_view', args=(slugify(data['name']),)))
        self.assertTrue(response)
        self.assertEquals(response.status_code, 404)