from django.conf import settings
from django.template.loader import render_to_string
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class EmailHelper:
    def __init__(self, subject, template_file, ctx=None, sender=None, receivers=None):
        self.subject = f'RememberME - {subject}'
        self.template_file = template_file
        self.ctx = ctx or {}
        self.sender = sender or settings.DEV_EMAIL
        self.receivers = receivers or [settings.ADMIN_EMAIL]

    def send(self):
        try:
            message = Mail(
                from_email=self.sender,
                to_emails=self.receivers,
                subject=self.subject,
                html_content=render_to_string(self.template_file, self.ctx)
            )
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            sg.send(message)
        except Exception as e:
            print(e)
