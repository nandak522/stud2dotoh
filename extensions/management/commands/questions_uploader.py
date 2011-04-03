import os
from optparse import make_option
from django.core.management.base import BaseCommand
import csv
from quest.models import Question, QuestionAlreadyExistsException
from users.models import UserProfile
from taggit.managers import TaggableManager
from .common import Spec, SpecColumn

class QuestionsSpec(Spec):
    SERIAL = SpecColumn(header_name='Serial No.', length=10, data_type=int, required=False)
    TITLE = SpecColumn(header_name='Question Title', length=80, data_type=str, required=True)
    TAGS = SpecColumn(header_name='Tags', length=100, data_type=int, required=False)

FIELD_LENGTHS = {'Question Title':80, 'Tags':100}

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--path', action='store', dest='path', help='Supply the Absolute Path of the import file'),
        make_option('--start', action='store', dest='start', help='Start Record'),
        make_option('--end', action='store', dest='end', help='End Record'),
    )
    help = "This Commands uploads Questions from a CSV file"

    requires_model_validation = True

    def handle(self, *args, **options):
        csv_file_path = options['path']
        if not os.path.exists(csv_file_path):
            print 'Supplied CSV file %s doesn\'t exist. Please give correct path'
        start = options['start']
        start = int(start) if start else 0
        end = options['end']
        end = int(end) if end else -1
        self.userprofile = UserProfile.objects.get(user__email='madhav.bnk@gmail.com')
        spec = QuestionsSpec(csv_file_path)
        spec.validate()
        cleaned_data = spec.cleaned_data
        import pdb
        pdb.set_trace()
        counter = 0
        if start:
            for record_number in range(start-1):
                cleaned_data.next()
                counter += 1
        import pdb
        pdb.set_trace()
        while end == -1 or counter < end:
            try:
                question_details = cleaned_data.next()
            except StopIteration:
                break
            self.creation_question(question_details)

    def creation_question(self, questions_details):
        title = questions_details['Question Title']
        tags_names = [tag_name.strip() for tag_name in questions_details['Tags'].split(',')] if questions_details['Tags'] else ()
        try:
            Question.objects.create_question(title, '', self.userprofile, tags_names)
            print 'Question %s saved' % question_details['Serial No']
        except QuestionAlreadyExistsException:
            pass