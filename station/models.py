from django import views
from django.contrib.auth.models import User
from django.contrib.auth.models import models
from geopy.geocoders import Nominatim
import geocoder
from django.db.models import Count
from django.utils.text import slugify
from autoslug import AutoSlugField
from django.template.defaultfilters import slugify
from django.utils.text import slugify


def get_default_location():
    location = geocoder.ip('me')
    if location is not None:
        latitude = location.lat
        longitude = location.lng
        return str(latitude), str(longitude)
    return "", ""


from django.template.defaultfilters import slugify

def generate_unique_slug(instance, field_name, max_length=255):
    value = getattr(instance, field_name)
    slug = slugify(value)[:max_length]
    unique_slug = slug
    num = 1
    model = instance.__class__
    while model.objects.filter(slug=unique_slug).exclude(id=instance.id).exists():
        unique_slug = f"{slug}-{num}"
        num += 1
    return unique_slug


# Create your models here.
class Station(models.Model):
    STATUS_CHOICES = (
        ("Actif", "Actif"),
        ("NonActif", "NonActif"),
    )
    
    nom = models.CharField(max_length=55)
    localisation = models.CharField(max_length=55)
    nni = models.CharField(max_length=55)
    email = models.EmailField(max_length=32)
    telephone = models.CharField(max_length=10)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES)
    typeCarburant = models.CharField(max_length=100)
    modePaiyement = models.CharField(max_length=100)
    latitude = models.CharField(default=get_default_location()[0])
    longitude = models.CharField(default=get_default_location()[1])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = AutoSlugField(unique=True, populate_from='id')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, 'id')
        super().save(*args, **kwargs)

    





