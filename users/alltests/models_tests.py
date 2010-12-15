from utils import TestCase
from users.models import UserProfile, Student, College, Professor

class UserProfileCreationTests(TestCase):
    fixtures = ['users.json']

    def test_userprofile_valid_creation(self):
        data = {'email':'nandakishore@gmail.com',
                'password':'somevalidpasssword',
                'name':'Madhav'}
        UserProfile.objects.create_profile(**data)
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
                          **data)
        
class StudentCreationTests(TestCase):
    fixtures = ['users.json', 'colleges.json', 'students.json']
    
    def test_student_valid_creation(self):
        data = {'userprofile':UserProfile.objects.get(slug='nanda-kishore'),
                'branch':'CSE',
                'college':College.objects.latest(),
                'start_year':2006,
                'end_year':2010}
        Student.objects.create_student(**data)
        student = Student.objects.latest()
        self.assertTrue(student)
        self.assertEquals(student.userprofile, data['userprofile'])
        self.assertEquals(student.branch, data['branch'])
        self.assertEquals(student.college, data['college'])
        self.assertEquals(student.start_year, data['start_year'])
        self.assertEquals(student.end_year, data['end_year'])
    
    def test_student_duplicate_creation(self):
        data = {'userprofile':UserProfile.objects.get(slug='somerandomuser'),
                'branch':'CSE',
                'college':College.objects.latest(),
                'start_year':2006,
                'end_year':2010}
        from users.models import StudentAlreadyExistsException
        self.assertRaises(StudentAlreadyExistsException,
                          Student.objects.create_student,
                          **data)
    
class CollegeCreationTests(TestCase):
    fixtures = ['colleges.json']
    
    def test_college_valid_creation(self):
        data = {'name':'SVPCET'}
        College.objects.create_college(name=data['name'])
        college = College.objects.latest()
        self.assertTrue(college)
        self.assertEquals(college.name, data['name'])
    
    def test_college_duplicate_creation(self):
        data = {'name':'JNTU Hyderabad'}
        from users.models import CollegeAlreadyExistsException
        self.assertRaises(CollegeAlreadyExistsException,
                          College.objects.create_college,
                          **data)
    
class ProfessorCreationTests(TestCase):
    fixtures = ['users.json', 'colleges.json', 'profs.json']
    
    def test_prof_valid_creation(self):
        data = {'userprofile':UserProfile.objects.get(slug='nanda-kishore'),
                'college':College.objects.get(slug='jntu-hyderabad')}
        Professor.objects.create_professor(**data)
        prof = Professor.objects.latest()
        self.assertTrue(prof)
        self.assertEquals(prof.userprofile, data['userprofile'])
        self.assertEquals(prof.college, data['college'])
    
    def test_prof_duplicate_creation(self):
        data = {'userprofile':UserProfile.objects.get(slug='somerandomuser'),
                'college':College.objects.get(slug='jntu-hyderabad')}
        from users.models import ProfessorAlreadyExistsException
        self.assertRaises(ProfessorAlreadyExistsException,
                          Professor.objects.create_professor,
                          **data)