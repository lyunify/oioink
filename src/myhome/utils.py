from django.core.mail import EmailMessage
from django.conf import settings


def send_contact_form(request, contact):
    email_subject = f"{contact['name']} from {contact['email']}: {contact['subject']}"
    email_body = contact['message']
    email_from = settings.EMAIL_FROM_USER
    email_to = [settings.EMAIL_FROM_USER]
    email = EmailMessage(email_subject, email_body, email_from, email_to)
    sent_status = email.send(fail_silently=False)
    return sent_status
