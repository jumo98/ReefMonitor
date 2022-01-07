from django.conf import settings

from mailjet_rest import Client
import os

from reefmonitor.apps.rules.models import Violation

class EMailHandler():
    mailjet = Client(auth=(settings.MAILJET_KEY, settings.MAILJET_SECRET), version='v3.1')
    
    def Send(self, violations: Violation):
        msg = ""

        for violation in violations:
            msg += f"{violation.timestamp}<br />"

        data = {
        'Messages': [
            {
            "From": {
                "Email": "julian.motz@iubh.de",
                "Name": "ReefMonitor"
            },
            "To": [
                {
                "Email": "julmotz@gmx.de",
                "Name": "Julian"
                }
            ],
            "Subject": "Greetings from Mailjet.",
            "TextPart": "My first Mailjet email",
            "HTMLPart": "<h3>Dear passenger 1, welcome to <a href='https://www.mailjet.com/'>Mailjet</a>!</h3><br />May the delivery force be with you!<br />" + msg,
            "CustomID": "AppGettingStartedTest"
            }
        ]
        }
        result = self.mailjet.send.create(data=data)
        print(result.status_code)
        print(result.json())