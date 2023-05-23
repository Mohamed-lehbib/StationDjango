from django.contrib.auth.models import User
from django.contrib.auth.models import models


# Create your models here.
class Station(models.Model):
    STATUS_CHOICES = (
        ("Actif", "Actif"),
        ("NonActif", "NonActif"),
    )
    nni = models.CharField(max_length=10)
    nom = models.CharField(max_length=55)
    localisation = models.CharField(max_length=55)
    email = models.EmailField(max_length=32)
    telephone = models.CharField(max_length=10)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES)
    typeCarburant = models.CharField(max_length=100)
    modePaiyement = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.nom + " " + self.localisation + " " + self.telephone
