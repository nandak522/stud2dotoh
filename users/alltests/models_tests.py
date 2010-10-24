from utils import TestCase
from users.models import UserProfile

class UserProfileCreationTests(TestCase):
    fixtures = ['users.json']

    def test_userprofile_valid_creation(self):
        data = {'username':'nanda.kishore',
                'password':'somevalidpasssword',
                'email':'nandakishore@gmail.com',
                'name':'Madhav'}
        UserProfile.objects.create_userprofile(username=data['username'],
                                               password=data['password'],
                                               email=data['email'],
                                               name=data['name'])
        userprofile = UserProfile.objects.latest()
        self.assertTrue(userprofile)
        self.assertEquals(userprofile.user.username, data['username'])
        self.assertTrue(userprofile.check_password(data['password']))
        self.assertEquals(userprofile.user.email, data['email'])
        self.assertEquals(userprofile.name, data['name'])
        
    def test_userprofile_duplicate_creation(self):
        data = {'username':'madhavbnk',
                'password':'somevalidpasssword',
                'email':'madhav.bnk@gmail.com',
                'name':'Madhav'}
        from users.models import UserProfileAlreadyExistsException
        self.assertRaises(UserProfileAlreadyExistsException,
                          UserProfile.objects.create_userprofile,
                          username=data['username'],
                          password=data['password'],
                          email=data['email'],
                          name=data['name'])