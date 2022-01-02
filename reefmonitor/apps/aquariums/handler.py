from django.utils import timezone

from .models import Aquarium
from .db import TimeseriesDatabase

class Handler():
    def __init__(self, id):
        self.aquarium: Aquarium = Aquarium.objects.get(id=id)
        self.db = TimeseriesDatabase(self.aquarium.name, self.aquarium.id)

    def GetMeasurements(self, start_time, end_time):
        return self.db.GetMeasurements(start_time, end_time)

    def GetLatestMeasurements(self):
        return self.db.GetLatestMeasurements()

    def AddMeasurement(self, measurement):
        self.db.AddMeasurement(measurement)
        self.aquarium.update_date = timezone.now()
        self.aquarium.save()
        return 

    def Delete(self):
        self.aquarium.delete()
        self.db.DeleteDatabase()
        return 