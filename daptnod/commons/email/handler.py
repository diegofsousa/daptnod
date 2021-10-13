import enum
from django.conf import settings
from .dispatcher import html_send_email, simple_send_email

class EmailTemplateFile(enum.Enum):
    EmailVerification = 'email/email_verification.html'
    EmailChangedNotification = 'email/email_changed_notification.html'

class EmailSubject(enum.Enum):
    EmailVerification = '[DAPTNOD] Can we activate your account now?'
    EmailChangedNotification = '[DAPTNOD] A new email has been linked to your account'


def email_verification(name, target_email, activation_hash):
    context = {
		"name":name,
		"path_link": settings.LINK_VALIDATE_REGISTER,
		"link":activation_hash
	}
    html_send_email(EmailSubject.EmailVerification.value, EmailTemplateFile.EmailVerification.value, context, target_email)

def email_changed_notification(name, target_email, new_email):
    context = {
		"name":name,
		"site_link": settings.MAIN_HOST,
		"new_email":new_email
	}
    html_send_email(EmailSubject.EmailChangedNotification.value, EmailTemplateFile.EmailChangedNotification.value, context, target_email)
