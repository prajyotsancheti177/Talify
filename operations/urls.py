from django.contrib import admin
from django.urls import include, path
from .views import *

urlpatterns = [
    path('', home, name='home'),  
]