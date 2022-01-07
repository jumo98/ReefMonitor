from django.db import models
from django.utils import timezone
from reefmonitor.apps.aquariums.models import Aquarium

from reefmonitor.apps.rules.models import Violation

import uuid

# Create your models here.
class Timeout(models.Model):
    id = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4, primary_key=True)
    aquarium = models.ForeignKey(Aquarium, on_delete=models.CASCADE)
    start = models.DateTimeField()
    duration = models.DurationField()
    violations = models.ManyToManyField(Violation)

    def AddViolation(self, violation: Violation):
        self.violations.add(violation)

    def IsOver(self) -> bool:
        if timezone.now() - self.start >= self.duration:
            return True
        else:
            return False