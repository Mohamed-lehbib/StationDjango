from django.urls import path, include
from . import views

urlpatterns = [
    path('home',views.home, name="home"),
    path('',views.landingpage, name="landingpage"),
    path('signin',views.signin, name="signin"),
    path('signup',views.signup, name="signup"),
    path('signout',views.signout, name="signout"),
    path('signinStation', views.signinStation, name="signinStation"),
    path('signupStation', views.signupStation, name="signupStation" ),
    path('homeStation' ,views.homeStation, )
]