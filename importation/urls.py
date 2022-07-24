from django.contrib import admin
from django.urls import path, include

from components import authenticate
from . import views

urlpatterns = [
    path(r'importer', views.index, name="importer"),
]