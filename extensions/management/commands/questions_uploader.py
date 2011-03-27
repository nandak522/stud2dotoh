import os
from optparse import make_option
from django.core.management.base import BaseCommand
import csv
from quest.models import Question, QuestionAlreadyExistsException
from users.models import UserProfile
from taggit.managers import TaggableManager

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
        reader = csv.DictReader(open(csv_file_path, 'r'),
                                fieldnames=('Serial No', 'Question Title', 'Tags'))
        reader.next()
        counter = 0
        if start:
            for record_number in range(start-1):
                reader.next()
                counter += 1
                print counter
        import pdb
        pdb.set_trace()
        while end == -1 or counter < end:
            try:
                question_details = reader.next()
                for field_name,field_length in FIELD_LENGTHS.items():
                    if question_details.has_key(field_name):
                        if field_length >= len(question_details.get(field_name)):
                            continue
                        else:
                            raise Exception, "Given content '%s' exceeds allocated Length of %s" % (question_details.get(field_name), field_
                self.creation_question(question_details)
                print 'Question %s saved' % question_details['Serial No']
        reader.next()
        counter = 0
        if start:
            for record_number in range(start-1):
                reader.next()
            for record_number in range(start-1):
                reader.next()
                counter += 1
                print counter
        import pdb
        pdb.set_trace()
        while end == -1 or counter < end:
            try:
                question_details = reader.next()
                for field_name,field_length in FIELD_LENGTHS.items():
                    if question_details.has_key(field_name):
                        if field_length >= len(question_details.get(field_name)):
                            continue
                        else:
                            raise Exception, "Given content '%s' exceeds allocated Length of %s" % (question_details.get(field_name), field_
                self.creation_question(question_details)
                print 'Question %s saved' % question_details['Serial No']
                counter += 1
            except StopIteration:
                break
            except Exception,e:
                counter += 1
                print 'Question:%s Exception:%s' % (counter, e.__str__())

    def creation_question(self, questions_details):
        title = questions_details['Question Title']
        tags_names = [tag_name.strip() for tag_name in questions_details['Tags'].split(',')] if questions_details['Tags'] else ()
        try:
            Question.objects.create_question(title, '', self.userprofile, tags_names)
        except QuestionAlreadyExistsException:
            pass

