from django.core.mail import send_mail, send_mass_mail
from django.conf import settings

def default_emailer(from_email, to_emails, message, from_name='', subject=''):
    send_mail(subject, message, clean_from_email(from_email, from_name), to_emails)
    
def mail_admins(from_email, message, from_name='', subject=''):
    messages_info = []
    for admin in settings.ADMINS:
        messages_info.append((subject, message, clean_from_email(from_email, from_name), [admin[1]]))
    send_mass_mail(messages_info)
    
def clean_from_email(from_email, from_name=''):
    return "%s<%s>" % (from_name, from_email) if from_name else from_email