from django import forms

from .models import (
    Station,
)

class StationForm(forms.ModelForm):
    class Meta:
        model = Station
        fields = ["nom", "telephone", "localisation", "email", "typeCarburant", "modePaiyement"]