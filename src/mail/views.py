from django.shortcuts import render, redirect
from django.core.mail import send_mail


# Create your views here.

def mail_view(request):
    if not request.user.is_authenticated:
        return redirect('myhome:home')
    return render(request, 'mail/mail.html')


# -------------------------------------------------------------------------------------------------
# sample functions

# Your view or function where you want to send the email
def send_email_view(request):
    subject = 'Subject of the Email'
    message = 'Body of the Email'
    from_email = 'your_email@example.com'
    recipient_list = ['recipient1@example.com', 'recipient2@example.com']
    send_mail(subject, message, from_email, recipient_list)
    # Optionally, you can include HTML content:
    # send_mail(subject, message, from_email, recipient_list, html_message='<p>This is an HTML message.</p>')
    # Optionally, you can specify fail_silently=True to suppress exceptions
    # send_mail(subject, message, from_email, recipient_list, fail_silently=True)
    # Add any additional logic or return a response as needed
    return

# Your view or function where you want to send the email
def send_email(request):
    subject = 'Subject of the email'
    message = 'This is the message body.'
    from_email = 'your_email@example.com'
    recipient_list = ['recipient1@example.com', 'recipient2@example.com']
    # Sending the email
    send_mail(subject, message, from_email, recipient_list)
    return
