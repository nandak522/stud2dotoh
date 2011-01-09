from utils import TestCase
from utils import slugify
from users.models import UserProfile, AcadInfo, College, WorkInfo, Company

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
        
    def test_make_student(self):
        userprofile = UserProfile.objects.get(user__email='madhav.bnk@gmail.com')
        self.assertFalse(userprofile.is_student)
        userprofile.make_student()
        self.assertTrue(UserProfile.objects.get(user__email='madhav.bnk@gmail.com').is_student)
        
    def test_make_professor(self):
        userprofile = UserProfile.objects.get(user__email='madhav.bnk@gmail.com')
        self.assertFalse(userprofile.is_professor)
        userprofile.make_professor()
        self.assertTrue(UserProfile.objects.get(user__email='madhav.bnk@gmail.com').is_professor)
        
    def test_make_employee(self):
        userprofile = UserProfile.objects.get(user__email='madhav.bnk@gmail.com')
        self.assertFalse(userprofile.is_employee)
        userprofile.make_employee()
        self.assertTrue(UserProfile.objects.get(user__email='madhav.bnk@gmail.com').is_employee)
        
class AcadInfoCreationTests(TestCase):
    fixtures = ['users.json', 'colleges.json', 'acadinfo.json']
    
    def test_acadinfo_valid_creation(self):
        userprofile = UserProfile.objects.get(slug='nanda-kishore')
        data = {'userprofile':userprofile,
                'branch':'CSE',
                'college':College.objects.latest(),
                'start_year':2006,
                'end_year':2010}
        AcadInfo.objects.create_acadinfo(**data)
        acad_details = userprofile.acad_details
        self.assertTrue(acad_details)
        self.assertEquals(AcadInfo.objects.latest().userprofile, data['userprofile'])
        self.assertEquals(acad_details.branch, data['branch'])
        self.assertEquals(acad_details.college.slug, data['college'].slug)
        self.assertEquals(acad_details.start_year, data['start_year'])
        self.assertEquals(acad_details.end_year, data['end_year'])
    
    def test_acadinfo_duplicate_creation(self):
        data = {'userprofile':UserProfile.objects.get(slug='somerandomuser'),
                'branch':'CSE',
                'college':College.objects.latest(),
                'start_year':2006,
                'end_year':2010}
        from users.models import AcadInfoAlreadyExistsException
        self.assertRaises(AcadInfoAlreadyExistsException,
                          AcadInfo.objects.create_acadinfo,
                          **data)
    
class CollegeCreationTests(TestCase):
    fixtures = ['colleges.json']
    
    def test_college_valid_creation(self):
        data = {'name':'SVPCET'}
        College.objects.create_college(name=data['name'])
        college = College.objects.latest()
        self.assertTrue(college)
        self.assertEquals(college.name, data['name'])
        self.assertEquals(college.slug, slugify(data['name']))
    
    def test_college_duplicate_creation(self):
        data = {'name':'JNTU Hyderabad'}
        from users.models import CollegeAlreadyExistsException
        self.assertRaises(CollegeAlreadyExistsException,
                          College.objects.create_college,
                          **data)
    
class CompanyCreationTests(TestCase):
    fixtures = ['companies.json']
    
    def test_company_valid_creation(self):
        data = {'name':'Infosys'}
        Company.objects.create_company(**data)
        company = Company.objects.latest()
        self.assertTrue(company)
        self.assertEquals(company.name, data['name'])
        self.assertEquals(company.slug, slugify(data['name']))
        
    def test_duplicate_company_creation(self):
        data = {'name':'IBM'}
        from users.models import CompanyAlreadyExistsException
        self.assertRaises(CompanyAlreadyExistsException,
                          Company.objects.create_company,
                          **data)

class WorkInfoCreationTests(TestCase):
    fixtures = ['users.json', 'companies.json', 'colleges.json', 'workinfo.json']
    
    def test_workinfo_valid_creation(self):
        workplaces = [{'userprofile': UserProfile.objects.get(user__email='somerandomuser@gmail.com'),
                       'workplace': Company.objects.latest(),
                       'designation': 'Software Developer',
                       'years_of_exp':2},
                      {'userprofile': UserProfile.objects.get(user__email='pavani.sharma@gmail.com'),
                       'workplace': College.objects.latest(),
                       'designation': 'Computer Science Professor',
                       'years_of_exp':4}]
        for workplace_data in workplaces:
            WorkInfo.objects.create_workinfo(**workplace_data)
            workinfo = WorkInfo.objects.latest()
            self.assertTrue(workinfo)
            self.assertEquals(workinfo.userprofile, workplace_data['userprofile'])
            self.assertEquals(workinfo.workplace, workplace_data['workplace'])
            self.assertEquals(workinfo.designation, workplace_data['designation'])
            self.assertEquals(workinfo.years_of_exp, workplace_data['years_of_exp'])
        
    def test_duplicate_workinfo_creation(self):
        data = {'userprofile': UserProfile.objects.get(user__email='madhav.bnk@gmail.com'),
                'workplace': Company.objects.latest(),
                'designation': 'Software Developer',
                'years_of_exp':2}
        from users.models import WorkInfoAlreadyExistsException
        self.assertRaises(WorkInfoAlreadyExistsException,
                          WorkInfo.objects.create_workinfo,
                          **data)