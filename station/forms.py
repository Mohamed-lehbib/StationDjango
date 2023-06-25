from django import forms

from .models import (
    Station,
)

class StationForm(forms.ModelForm):
    class Meta:
        model = Station
        fields = ["nom","localisation" , "nni", "email","telephone", "status", "typeCarburant", "modePaiyement","latitude", "longitude"]