from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User

from reefmonitor.apps.rules.models import Violation

class EMailHandler():
    
    def Send(self, user: User, violations: Violation):
        msg = ""

        for violation in violations:
            msg += f"{violation.timestamp}<br />"
        
        code = send_mail(
            f'Rule Violation',
            msg,
            f'ReefMonitor <{settings.EMAIL_SENDER}>',
            [user.email],
            fail_silently=False,
        )

        print(code)