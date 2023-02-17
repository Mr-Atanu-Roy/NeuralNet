from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import Usermanager

# from core.models import ChitChat
from accounts.utils import send_custom_email, BaseModel

import uuid

from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

otp_purpose_choices = (
    ("email_verification", "Email Verification"),
    ("reset_password", "Reset Password")
)


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    
    objects = Usermanager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = 'auth_user'
    
    def __str__(self):
        return self.email
    

class OTP(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    auth_token = models.UUIDField(default=uuid.uuid4)
    purpose = models.CharField(choices=otp_purpose_choices, max_length=255, default="email_verification")
    is_expired = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.auth_token)
    

#creating an OTP instance after a new User is created
@receiver(post_save, sender=User)
def user_created_handler(sender, instance, created, *args, **kwargs):
    if created:         
        newOTP = OTP(user=instance)
        newOTP.save()
        # newChitChat = ChitChat(user=User)
        # newChitChat.save()
        
        subject = "Greetings From NeuralNet"
        message = f"Hello!!! Thank you for signing up with NeuralNet {instance.first_name}.... You have signed up using email - {instance.email}, at {instance.date_joined}"
        send_custom_email(instance.email, subject, message)
        

#sending email based on purpose after an OTP instance is created
@receiver(post_save, sender=OTP)
def OTP_created_handler(sender, instance, created, *args, **kwargs):
    if created:         
        token = instance.auth_token        
        subject = instance.purpose
        
        if subject.lower() == "email_verification":
            message = f"Your OTP for verifying email - {instance.user} is : {token}. This OTP is valid for the next 10 mintutes only"
            
        elif subject.lower() == "reset_password":
            message = f"Your OTP for reseting password for email - {instance.user} is : {token}. This OTP is valid for the next 10 mintutes only"
            
        send_custom_email(instance.user, subject, message)