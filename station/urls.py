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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home', views.home, name="home"),
    #path('', views.landingpage, name="landingpage"),
    path('signin', views.signin, name="signin"),
    path('signup', views.signup, name="signup"),
    path('signout', views.signout, name="signout"),
    path('homeStation', views.homeStation, name="homeStation"),  
    path('station/ajouter', StationCreate.as_view(), name="station_create"),
    path('index', views.index, name='index'),
    path('station/<slug:slug>/', views.station_detail, name='station-detail'),
    path('', dex, name='home'),
    path('<int:myid>', detail, name="detail"),
    path('checkout', checkout, name="checkout"),
    path('confirmation', confirmation, name="confirmation" ),
    path('addProduct', add_product, name="add_product"),
    path('all/commands/', all_commands, name='all_commands'),
    path('ajouter_panier/<int:product_id>/', ajouter_panier, name='ajouter_panier'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)