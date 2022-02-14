from django.utils import timezone

from ..notifications.handler import NotificationHandler
from ..rules.models import Rule, Violation
from .models import Aquarium, Measurement
from .db import TimeseriesDatabase

from typing import List

class Handler():
    def __init__(self, id):
        self.aquarium: Aquarium = Aquarium.objects.get(id=id)
        self.db = TimeseriesDatabase(self.aquarium.name, self.aquarium.id)

    def GetMeasurements(self, start_time, end_time) -> List[Measurement]:
        return self.db.GetMeasurements(start_time, end_time)

    def GetLatestMeasurements(self) -> List[Measurement]:
        return self.db.GetLatestMeasurements()

    def AddMeasurement(self, measurement: Measurement, external: bool):
        self.db.AddMeasurement(measurement)

        notifyHandler = NotificationHandler(self.aquarium)

        for param in measurement.parameters.all():
            rules = Rule.objects.filter(aquarium=self.aquarium, parameter=param.name)
            for rule in rules:
                if rule.Violates(param.value):
                    # Create new violation
                    violation = Violation(aquarium=self.aquarium, rule=rule, timestamp=timezone.now(), value=param.value)
                    violation.save()

                    if external:
                        notifyHandler.SendNotification(violation)

        self.aquarium.update_date = timezone.now()
        self.aquarium.save()
        return 

    def Delete(self):
        self.aquarium.delete()
        self.db.DeleteDatabase()
        return 