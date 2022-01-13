from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from reefmonitor.apps.aquariums.models import Aquarium, Measurement, Parameter

class AquariumTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('myuser', 'myemail@test.com', 'mypassword')
        Aquarium.create(name='MyAquarium', owner=self.user)

    def test_retrieve_user(self):
        aquarium = Aquarium.objects.get(name='MyAquarium')
        self.assertEqual(aquarium.owner, self.user)

    def test_retrieve_aquarium_for_user(self):
        aquarium = Aquarium.objects.get(name='MyAquarium')
        aq = Aquarium.objects.get(owner=self.user)
        self.assertEqual(aquarium, aq)

class ParameterTestCase(TestCase):
    def setUp(self):
        self.parameter_salinity = Parameter.objects.create(name=Parameter.Name.SALI, value=1.024)
        self.parameter_temperature = Parameter.objects.create(name=Parameter.Name.TEMP, value=26.5)

    def test_get_parameter_value(self):
        self.assertEqual(1.024, self.parameter_salinity.value)
        self.assertEqual(26.5, self.parameter_temperature.value)

    def test_display_parameter_name(self):
        self.assertEqual('Salinity', self.parameter_salinity.DisplayName(self.parameter_salinity.name))
        self.assertEqual('Temperature', self.parameter_temperature.DisplayName(self.parameter_temperature.name))

    def test_display_parameter_unit(self):
        self.assertEqual('g/l', self.parameter_salinity.DisplayUnit(self.parameter_salinity.name))
        self.assertEqual('°C', self.parameter_temperature.DisplayUnit(self.parameter_temperature.name))

class MeasurementTestCase(TestCase):
    def setUp(self):
        self.parameter_salinity = Parameter.objects.create(name=Parameter.Name.SALI, value=1.024)
        self.parameter_temperature = Parameter.objects.create(name=Parameter.Name.TEMP, value=26.5)
        self.measurement = Measurement.objects.create(timestamp=timezone.now())
        self.measurement.parameters.add(self.parameter_salinity)
        self.measurement.parameters.add(self.parameter_temperature)

    def test_get_parameters(self):
        parameters = self.measurement.parameters.all()
        for parameter in parameters:
            if parameter.name == "Salinity":
                self.assertEqual(parameter, self.parameter_salinity)
            else:
                self.assertEqual(parameter, self.parameter_temperature)