from datetime import timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from reefmonitor.apps.aquariums.models import Aquarium, Parameter
from reefmonitor.apps.notifications.models import Timeout
from reefmonitor.apps.rules.models import Rule, Violation

# Create your tests here.
class TimeoutTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user('myuser', 'myemail@test.com', 'mypassword')
        self.aquarium = Aquarium.create(name='MyAquarium', owner=user)

    def test_retrieve_and_check_if_over(self):
        start_now = timezone.now()
        duration = timedelta(seconds=30)
        start_past = start_now - duration
        Timeout.objects.create(aquarium=self.aquarium, start=start_now, duration=duration)

        timeout = Timeout.objects.get(aquarium=self.aquarium)
        self.assertEqual(False, timeout.IsOver())
        timeout.delete()

        Timeout.objects.create(aquarium=self.aquarium, start=start_past, duration=duration)
        timeout = Timeout.objects.get(aquarium=self.aquarium)
        self.assertEqual(True, timeout.IsOver())
        timeout.delete()

    def test_add_and_retrieve_violations(self):
        self.rule = Rule.objects.create(aquarium=self.aquarium, type=Rule.Type.MIN, value=1.02, parameter=Parameter.Name.SALI)
        violation_1 = Violation.objects.create(aquarium=self.aquarium, rule=self.rule, timestamp=timezone.now(), value=1)
        violation_2 = Violation.objects.create(aquarium=self.aquarium, rule=self.rule, timestamp=timezone.now(), value=0.5)
        

        start_now = timezone.now()
        duration = timedelta(seconds=30)
        Timeout.objects.create(aquarium=self.aquarium, start=start_now, duration=duration)

        timeout = Timeout.objects.get(aquarium=self.aquarium)
        self.assertEqual(False, timeout.IsOver())

        if not timeout.IsOver():
            timeout.AddViolation(violation_1)

        if not timeout.IsOver():
            timeout.AddViolation(violation_2)

        self.assertEqual(2, timeout.violations.all().count())
        