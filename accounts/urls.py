from django.urls import path

from .views import *

urlpatterns = [
    path('login/', login, name="login"),
    path('signin/', signin, name="signin"),
    path('logout/', logout, name="logout"),
    path('profile/', profile, name="profile"),
    path('email-verify/', email_verify, name="email-verify"),
    path('reset-password/', reset_password, name="reset-password"),
]
