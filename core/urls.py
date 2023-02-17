from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('product/chitchat/', chitchat, name="chitchat"),
    path('product/codegenie/', codegenie, name="codegenie"),
    path('product/artiflex/', artiflex, name="artiflex"),
]