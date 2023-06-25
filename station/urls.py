'''from django.urls import path, include
from . import views

from .views import (
    StationCreate,
)
urlpatterns = [
    path('home',views.home, name="home"),
    path('',views.landingpage, name="landingpage"),
    path('signin',views.signin, name="signin"),
    path('signup',views.signup, name="signup"),
    path('signout',views.signout, name="signout"),
    path('signinStation', views.signinStation, name="signinStation"),
    path('signupStation', views.signupStation, name="signupStation" ),
    path('homeStation' ,views.homeStation, )
    path('station_form' ,views.station_form, )
    path("station/ajouter", StationCreate.as_view(), name="station-create"),
]'''

from django.urls import path, include
from . import views

from station.views import *
from .views import StationCreate 

urlpatterns = [
    path('home', views.home, name="home"),
    path('', views.landingpage, name="landingpage"),
    path('signin', views.signin, name="signin"),
    path('signup', views.signup, name="signup"),
    path('signout', views.signout, name="signout"),
    path('signinStation', views.signinStation, name="signinStation"),
    path('signupStation', views.signupStation, name="signupStation"),
    path('homeStation', views.homeStation, name="homeStation"),  
    path('station/ajouter', StationCreate.as_view(), name="station_create"),
    path('index', views.index, name='index'),
    path('station/<slug:slug>/', views.station_detail, name='station-detail'),
]
