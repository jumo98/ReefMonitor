from django.utils import timezone
import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Aquarium(models.Model):
    class Meta: 
        verbose_name = "Aquarium"
        verbose_name_plural = "Aquariums"

    def create(name, owner):
        aq = Aquarium(name=name, owner=owner, create_date=timezone.now(), update_date=timezone.now())
        aq.save()
        return aq
        

    name = models.CharField(max_length=24)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4, primary_key=True)
    create_date = models.DateTimeField('date created')
    update_date = models.DateTimeField('date updated')

    def __str__(self):
        return self.name

    def __id__(self):
        return self.id

class Parameter(models.Model):
    class Meta: 
        verbose_name = "Parameter"
        verbose_name_plural = "Parameters"

    class Name(models.TextChoices):
        SALI = 'Salinity', 'Salinity'
        TEMP = 'Temperature', 'Temperature'
        CARB = 'Carbonate Hardness', 'Carbonate Hardness'
        CALC = 'Calcium', 'Calcium'
        MAGN = 'Magnesium', 'Magnesium'

    
    class Units(models.TextChoices):
        SALI = 'Salinity', 'g/l'
        TEMP = 'Temperature', '°C'
        CARB = 'Carbonate Hardness', 'KH'
        CALC = 'Calcium', 'ppm'
        MAGN = 'Magnesium', 'ppm'

    name = models.CharField(max_length=48, choices=Name.choices, default=Name.TEMP)
    value = models.FloatField()

    def DisplayName(self, name):
        d = dict(self.Name.choices)
        if name in d:
            return d[name]
        return None

    def DisplayUnit(self, name):
        d = dict(self.Units.choices)
        if name in d:
            return d[name]
        return None

class Measurement(models.Model):
    class Meta: 
        verbose_name = "Measurement"
        verbose_name_plural = "Measurements"

    timestamp = models.DateTimeField('timestamp')
    parameters = models.ManyToManyField(Parameter)

