from datetime import datetime, timedelta

from django.utils import timezone
from reefmonitor.apps.notifications.email import EMailHandler
from reefmonitor.apps.rules.models import Violation
from .models import Timeout

class NotificationHandler():
    def __init__(self, aquarium):
        self.aquarium = aquarium
        self.notifiers = []
        # self.notifiers.append(EMailHandler())

    def SendNotification(self, violation: Violation):
        # Check for an existing timeout
        timeout = None
        try:
            timeout = Timeout.objects.get(aquarium=self.aquarium)
        except Timeout.DoesNotExist:
            pass

        # If an timeout exists:
        if timeout:
            #
            if timeout.IsOver():
                timeout.AddViolation(violation)
                violations = timeout.violations.all()
                for notifier in self.notifiers:
                    notifier.Send(violations)
                timeout.delete()
            else:
                timeout.AddViolation(violation)

        if timeout == None:
            for notifier in self.notifiers:
                notifier.Send([violation])
            timeout = Timeout(aquarium=self.aquarium, start=timezone.now(), duration=timedelta(minutes=30))
            timeout.save()
            timeout.AddViolation(violation)
            timeout.save()
        