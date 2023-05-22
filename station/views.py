import email
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render



from .models import Station

from .forms import StationForm

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
        if User.objects.filter(username= username):
            messages.error(request, "username already exist")
            return redirect('signup')
        
        if User.objects.filter(email= email):
            messages.error(request, "email already exist")
            return redirect('signup')

        if len(username)>10:
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
        
        #return redirect('/signin')
    return render(request, 'signup.html')

def signout(request):
    logout(request)
    return redirect('/')

#creation d'un login station
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

        if User.objects.filter(username= username):
            messages.error(request, "username already exist")
            return redirect('signupStation')
        
        if User.objects.filter(email= email):
            messages.error(request, "email already exist")
            return redirect('signupStation')

        if len(username)>10:
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
        
        #return redirect('/signin')
    return render(request, 'signupStation.html')
@login_required(login_url="/signinStation")
def homeStation(request):
    return render(request, 'homeStation.html')

class StationCreate(LoginRequiredMixin ,View):
    def get(self, request):
        form = StationForm()
        return render(request, "station_form.html", {"form": form})

    def post(self, request):
        form = StationForm(data=request.POST)
        
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect("homeStation")

        return render(request,"station_form.html", {"form": form})
    
   