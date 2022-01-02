import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Aquarium(models.Model):
    class Meta: 
        verbose_name = "Aquarium"
        verbose_name_plural = "Aquariums"

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
    class Name(models.TextChoices):
        SALI = 'salinity'
        TEMP = 'temperature'
        CARB = 'carbonate'
        CALC = 'calcium'
        MAGN = 'magnesium'

    name = models.CharField(max_length=48, choices=Name.choices, default=Name.TEMP)
    value = models.FloatField()

class Measurement(models.Model):
    timestamp = models.DateTimeField('timestamp')
    parameters = models.ManyToManyField(Parameter)

