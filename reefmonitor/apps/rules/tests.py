from django.utils import timezone
from django.contrib.auth.models import User
from django.test import TestCase
from reefmonitor.apps.aquariums.models import Aquarium, Parameter

from reefmonitor.apps.rules.models import Hint, Rule, Violation

# Create your tests here.
class RuleTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user('myuser', 'myemail@test.com', 'mypassword')
        self.aquarium = Aquarium.create(name='MyAquarium', owner=user)
        self.rule_min = Rule.objects.create(aquarium=self.aquarium, type=Rule.Type.MIN, value=1.02, parameter=Parameter.Name.SALI)
        self.rule_max = Rule.objects.create(aquarium=self.aquarium, type=Rule.Type.MAX, value=27.5, parameter=Parameter.Name.TEMP)

    def test_get_rules_for_aquarium(self):
        rules = Rule.objects.filter(aquarium=self.aquarium)

        for rule in rules:
            if rule.type == Rule.Type.MIN:
                self.assertEqual(rule.id, str(self.rule_min.id))
            else:
                self.assertEqual(rule.id, str(self.rule_max.id))

    def test_rule_violation_min(self):
        self.assertEqual(True, self.rule_min.Violates(1))
        self.assertEqual(False, self.rule_min.Violates(2))

    def test_rule_violation_max(self):
        self.assertEqual(True, self.rule_max.Violates(28))
        self.assertEqual(False, self.rule_max.Violates(25))

class HintTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user('myuser', 'myemail@test.com', 'mypassword')
        self.aquarium = Aquarium.create(name='MyAquarium', owner=user)
        self.rule = Rule.objects.create(aquarium=self.aquarium, type=Rule.Type.MIN, value=1.02, parameter=Parameter.Name.SALI)
        self.hint = Hint.objects.create(parameter=self.rule.parameter, type=self.rule.type, message="This is a hint!")

    def test_violation_hint_workflow(self):
        test_value = 1
        if self.rule.Violates(test_value):
            Violation.objects.create(aquarium=self.aquarium, rule=self.rule, timestamp=timezone.now(), value=test_value)
        
        # Retrieve violations for aquarium
        violations = Violation.objects.filter(aquarium=self.aquarium)

        # Expect one
        self.assertEqual(1, violations.count())

        # Retrieve hints for each violation
        for violation in violations:
            # Retrieve a hint
            hint = Hint.objects.get(parameter=violation.rule.parameter, type=violation.rule.type)
            self.assertEqual(self.hint.GetMessage(), hint.GetMessage())
            