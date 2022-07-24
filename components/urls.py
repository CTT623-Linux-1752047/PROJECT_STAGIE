from django.contrib import admin
from django.urls import path, include

from components import authenticate
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('/getData', views.getData, name="getData"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
]