from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('chitchat', chitchat, name="chitchat"),
    path('codegenie', codegenie, name="codegenie"),
    path('artiflex', artiflex, name="artiflex"),
]
