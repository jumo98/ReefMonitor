from django import forms
from django.utils import timezone

from .models import Aquarium, Measurement, Parameter

class AquariumForm(forms.Form):
    name = forms.CharField(max_length=24,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Aquarium",
                "class": "form-control"
            }
        ),
        required=True)

    def save(self, name, user):
        aquarium = Aquarium(name=name, owner=user, create_date=timezone.now(), update_date=timezone.now())
        aquarium.save()


class MeasurementForm(forms.Form):
    salinity = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "placeholder": "1.025",
                "class": "form-control"
            }
        ),
        required=False)
    
    temperature = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "placeholder": "25.6",
                "class": "form-control"
            }
        ),
        required=False)
    
    carbonate = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "placeholder": "Carbonate Hardness",
                "class": "form-control"
            }
        ),
        required=False)

    calcium = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "placeholder": "Calcium",
                "class": "form-control"
            }
        ),
        required=False)

    magnesium = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "placeholder": "Magnesium",
                "class": "form-control"
            }
        ),
        required=False)

    def ToMeasurement(self, timestamp) -> Measurement:
        measurement = Measurement()
        measurement.timestamp = timestamp
        measurement.save()
        

        params = []
        salinity = self.cleaned_data.get("salinity")
        if salinity:
            param = Parameter(name=Parameter.Name.SALI, value=salinity)
            param.save()
            params.append(param)

        temperature = self.cleaned_data.get("temperature")
        if temperature:
            param = Parameter(name=Parameter.Name.TEMP, value=temperature)
            param.save()
            params.append(param)

        carbonate = self.cleaned_data.get("carbonate")
        if carbonate:
            param = Parameter(name=Parameter.Name.CARB, value=carbonate)
            param.save()
            params.append(param)

        calcium = self.cleaned_data.get("calcium")
        if calcium:
            param = Parameter(name=Parameter.Name.CALC, value=calcium)
            param.save()
            params.append(param)

        magnesium = self.cleaned_data.get("magnesium")
        if magnesium:
            param = Parameter(name=Parameter.Name.MAGN, value=magnesium)
            param.save()
            params.append(param)

        measurement.parameters.set(params)

        return measurement