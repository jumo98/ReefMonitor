from django.db import models

from ..aquariums.models import Aquarium, Parameter

import uuid

# Create your models here.
class Rule(models.Model):
    class Meta: 
        verbose_name = "Rule"
        verbose_name_plural = "Rules"

    class Type(models.TextChoices):
        MIN = 'Minimum', 'Minimum'
        MAX = 'Maximum', 'Maximum'

    id = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4, primary_key=True)
    aquarium = models.ForeignKey(Aquarium, on_delete=models.CASCADE)
    
    value = models.FloatField()
    type = models.CharField(max_length=48, choices=Type.choices, default=Type.MIN)
    parameter = models.CharField(max_length=48, choices=Parameter.Name.choices, default=Parameter.Name.TEMP)

    def __id__(self):
        return self.id

    def Delete(self):
        return self.delete()

    def Violates(self, value):
        if self.type == self.Type.MIN:
            return value < self.value
        elif self.type == self.Type.MAX:
            return value > self.value
        else:
            return False

class Violation(models.Model):
    class Meta:
        verbose_name = "Violation"
        verbose_name_plural = "Violations"

    id = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4, primary_key=True)
    aquarium = models.ForeignKey(Aquarium, on_delete=models.CASCADE)
    rule = models.ForeignKey(Rule, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    value = models.FloatField()

