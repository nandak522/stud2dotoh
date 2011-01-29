from django.core.mail import send_mail, send_mass_mail
from django.conf import settings
from users.models import UserProfile

def default_emailer(from_email, to_emails, message, from_name='', subject=''):
    send_mail(subject, message, clean_from_email(from_email, from_name), to_emails)
    
def mail_admins(from_email, message, from_name='', subject=''):
    messages_info = []
    for admin in settings.ADMINS:
        messages_info.append((subject, message, clean_from_email(from_email, from_name), [admin[1]]))
    send_mass_mail(messages_info)
    
def clean_from_email(from_email, from_name=''):
    return "%s<%s>" % (from_name, from_email) if from_name else from_email

def mail_group(group_type, group, from_email, message, from_name='', subject=''):
    messages_info = []
    if group_type == 'college':
       userprofiles_ids = group.acadinfo_set.values('userprofile')
       userprofiles = UserProfile.objects.filter(id__in=[id_info['userprofile'] for id_info in userprofiles_ids])
       userprofiles = filter(lambda userprofile:userprofile.is_student, userprofiles)
    elif group_type == 'company':
        userprofiles = group.workinfo_set.values('userprofile')
        userprofiles = UserProfile.objects.filter(id__in=[id_info['userprofile'] for id_info in userprofiles_ids])
        userprofiles = filter(lambda userprofile:userprofile.is_employee, userprofiles)
    else:
        raise NotImplementedError
    emails = [userprofile.user.email for userprofile in userprofiles]
    for email in emails:
        messages_info.append((subject, message, clean_from_email(from_email, from_name), [email]))
    send_mass_mail(messages_info)