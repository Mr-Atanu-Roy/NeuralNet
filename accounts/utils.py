from django.conf import settings
from django.core.mail import send_mail

from django.db import models

#function to send email
def send_custom_email(receiver, subject, message):
    sender = settings.EMAIL_HOST_USER
    recipient_list = [receiver]
    
    send_mail(subject, message, sender, recipient_list)
    
    
#base model
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True