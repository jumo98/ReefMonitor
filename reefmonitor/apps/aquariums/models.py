import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Aquarium(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4, primary_key=True)

    create_date = models.DateTimeField('date created')
    update_date = models.DateTimeField('date updated')

    def __str__(self):
        return self.name

    def __id__(self):
        return self.id