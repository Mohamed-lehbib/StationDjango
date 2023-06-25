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
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User


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

    



# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_added']
    def str(self):
        return self.name    


class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.TextField()
    category = models.ForeignKey(Category, related_name='categorie', on_delete=models.CASCADE) 
    image = models.ImageField(upload_to='images/')  
    date_added = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    quantity = models.IntegerField(default=1)  # New field for quantity

    class Meta:
        ordering = ['-date_added']

    def str(self):
        return self.title

        

class Commande(models.Model):
    items = models.CharField(max_length=300)
    total = models.CharField(max_length=200)
    nom = models.CharField(max_length=150)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    ville = models.CharField(max_length=200)
    pays = models.CharField(max_length=300)
    zipcode = models.CharField(max_length=300)
    date_commande = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_commande']


    def str(self):
        return self.nom


