from django.core.mail import send_mail, send_mass_mail
from django.conf import settings
from users.models import UserProfile
from django.template.loader import render_to_string as render_template
#from django.core.validators import email_re
import re

EMAIL_REGEX = '[\w\.-]+@[a-zA-Z0-9]+[\.][a-zA-Z]{2,4}'
DEFAULT_FROM_EMAIL = 'do-not-reply@stud2dotoh.com'

def default_emailer(from_email, to_emails, message, from_name='', subject=''):
    send_mail(subject, message, address_email_with_name(from_email, from_name), to_emails)
    
def mail_admins(from_email, message, from_name='', subject=''):
    messages_info = []
    for admin in settings.ADMINS:
        messages_info.append((subject, message, address_email_with_name(from_email, from_name), [admin[1]]))
    send_mass_mail(messages_info)
    
def address_email_with_name(email, name=''):
    return "%s<%s>" % (name, email) if name else email

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
        messages_info.append((subject, message, address_email_with_name(from_email, from_name), [email]))
    send_mass_mail(messages_info)
    
def invitation_emailer(from_email, to_emails, from_name=''):
    message = render_template('emails/invitation.html', {'inviter_name':from_name,
                                                         'inviter_email':from_email}) 
    default_emailer(from_email=from_email,
                    to_emails=to_emails,
                    message=message,
                    from_name=from_name,
                    subject='Hi, This is %s' % from_name)
    
def clean_emails(multiple_emails_string):
    return re.findall(r'%s' % EMAIL_REGEX, multiple_emails_string)

def welcome_emailer(to_email, to_name):
    message = render_template('emails/welcome.html', {'name':to_name}) 
    default_emailer(from_email=DEFAULT_FROM_EMAIL,
                    to_emails=[address_email_with_name(to_email, to_name)],
                    message=message,
                    subject='Welcome to Stud2.0')