from django.core.mail import send_mail

def default_emailer(from_email, to_emails, message, subject=''):
    send_mail(subject, message, from_email, to_emails)