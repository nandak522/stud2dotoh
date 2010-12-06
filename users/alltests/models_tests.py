from utils import TestCase
from users.models import UserProfile

class UserProfileCreationTests(TestCase):
    fixtures = ['users.json']

    def test_userprofile_valid_creation(self):
        data = {'email':'nandakishore@gmail.com',
                'password':'somevalidpasssword',
                'name':'Madhav'}
        UserProfile.objects.create_profile(email=data['email'],
                                           password=data['password'],
                                           name=data['name'])
        userprofile = UserProfile.objects.latest()
        self.assertTrue(userprofile)
        self.assertTrue(userprofile.check_password(data['password']))
        self.assertEquals(userprofile.user.email, data['email'])
        self.assertEquals(userprofile.name, data['name'])
        
    def test_userprofile_duplicate_creation(self):
        data = {'email':'madhav.bnk@gmail.com',
                'password':'somevalidpasssword',
                'name':'Madhav'}
        from users.models import UserProfileAlreadyExistsException
        self.assertRaises(UserProfileAlreadyExistsException,
                          UserProfile.objects.create_profile,
                          email=data['email'],
                          password=data['password'],
                          name=data['name'])