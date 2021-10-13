from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

def html_send_email(subject, email_template, email_context_variables, target_emails):
    email_content = render_to_string(email_template, email_context_variables)
    
    email = EmailMessage(subject, email_content, settings.EMAIL_HOST_USER, [target_emails,])
    email.content_subtype = "html"
    email.send(fail_silently=False)

def simple_send_email(subject, email_content, target_emails):
    
    email = EmailMultiAlternatives(subject, email_content, settings.EMAIL_HOST_USER, [target_emails,])
    email.attach_alternative(email_content, "text/html")
    email.send()