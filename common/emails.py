from django.conf import settings
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import render_to_string


def send_registration_email(to, message):
    c = Context({'email': to, 'message': message})

    email_subject = "Welcome"
    email_body = message

    email = EmailMessage(
        email_subject, email_body, to=[to],
        reply_to=[to]
    )

    return email.send(fail_silently=False)
