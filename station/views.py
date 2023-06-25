from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
import folium
import geocoder
from .forms import StationForm
from .models import Station
from geopy.geocoders import Nominatim
from django.templatetags.static import static
from django.utils.text import slugify
from django.urls import reverse



# Create your views here.
@login_required(login_url="/signin")
def home(request):
    return render(request, 'home.html')


def landingpage(request):
    return render(request, 'landingpage.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        user = authenticate(username=username, password=password1)
        if user is not None:
            login(request, user)
            username = user.username
            return redirect('home')
        else:
            messages.error(request, "error")
            return redirect('signin')

    return render(request, 'signin.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if User.objects.filter(username=username):
            messages.error(request, "username already exist")
            return redirect('signup')

        if User.objects.filter(email=email):
            messages.error(request, "email already exist")
            return redirect('signup')

        if len(username) > 10:
            messages.error(request, "username is to long")
            return redirect('signup')

        if password1 != password2:
            messages.error(request, 'the password is not correct')
            return redirect('signup')

        if not username.isalnum():
            messages.error(request, 'the username should be an alnum')
            return redirect('signup')

        myuser = User.objects.create_user(username, email, password1)
        myuser.save()
        messages.success(request, "sucess")
        return redirect('signin')

        # return redirect('/signin')
    return render(request, 'signup.html')


def signout(request):
    logout(request)
    return redirect('/')


# creation d'un login station
def signinStation(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        user = authenticate(username=username, password=password1)
        if user is not None:
            login(request, user)
            username = user.username
            return redirect('homeStation')
        else:
            messages.error(request, "error")
            return redirect('signinStation')

    return render(request, 'signinStation.html')


def signupStation(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if User.objects.filter(username=username):
            messages.error(request, "username already exist")
            return redirect('signupStation')

        if User.objects.filter(email=email):
            messages.error(request, "email already exist")
            return redirect('signupStation')

        if len(username) > 10:
            messages.error(request, "username is to long")
            return redirect('signupStation')

        if password1 != password2:
            messages.error(request, 'the password is not correct')

        if not username.isalnum():
            messages.error(request, 'the username should be an alnum')
            return redirect('signupStation')

        myuser = User.objects.create_user(username, email, password1)
        myuser.is_staff = 1
        myuser.save()
        messages.success(request, "sucess")
        return redirect('signinStation')

        # return redirect('/signin')
    return render(request, 'signupStation.html')


@login_required(login_url="/signinStation")
def homeStation(request):
    stations = Station.objects.all()
    return render(request, 'homeStation.html', {"stations": stations})


class StationCreate(LoginRequiredMixin, View):
    def get(self, request):
        form = StationForm()
        return render(request, "station_form.html", {"form": form})

    def post(self, request):
        form = StationForm(data=request.POST)

        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect("index")

        return render(request, "station_form.html", {"form": form})



def index(request):
    if request.method == 'POST':
        form = StationForm(request.POST)
        if form.is_valid():
            station = form.save(commit=False)
            station.user = request.user
            station.save()
            return redirect('/')
    else:
        form = StationForm()

    stations = Station.objects.all()

    # Créer une carte avec des marqueurs pour les stations existantes
    m = folium.Map(location=[20, -10], zoom_start=6)
    for station in stations:
        
        
        
        
        # Generate the URL for the station's detail page
        station_url = reverse('station-detail', args=[station.slug])



        folium.Marker([station.latitude, station.longitude], tooltip=station.nom,
            popup=f'<a href="{station_url}">{station.nom}</a>'
        ).add_to(m)


    # Obtenir la localisation de l'utilisateur connecté
  
   
   
    m = m._repr_html_()

    context = {
        'form': form,
        'm': m
    }
    return render(request, 'index.html', context)
    


def get_default_location():
    location = geocoder.ip('me')
    if location is not None:
        return str(location)
    return ""


from django.shortcuts import render, get_object_or_404
from .models import Station



def station_detail(request, slug):
    station = get_object_or_404(Station, slug=slug)
    context = {
        'station': station
    }
    return render(request, 'station_detail.html',  context)
