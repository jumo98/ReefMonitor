from django import forms

from ..aquariums.models import Parameter
from .models import Rule

class RuleForm(forms.Form):
    value = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "placeholder": "1.025",
                "class": "form-control"
            }
        ),
        required=True)
    
    type = forms.ChoiceField(
        widget=forms.Select,
        choices=Rule.Type.choices,
        required=True)
    
    parameter = forms.ChoiceField(
        widget=forms.Select,
        choices=Parameter.Name.choices,
        required=True)

    def save(self, aquarium):
        rule = Rule(aquarium=aquarium, value=self.cleaned_data.get("value"), parameter=self.cleaned_data.get("parameter"), type=self.cleaned_data.get("type"))
        rule.save()
        return rule

    def update(self, id):
        rule = Rule.objects.get(id=id)
        rule.value = self.cleaned_data.get("value")
        rule.parameter = self.cleaned_data.get("parameter")
        rule.type = self.cleaned_data.get("type")
        rule.save()
        return rule
