from django.db import models

from django.contrib.auth import get_user_model #importing the User model
from accounts.utils import BaseModel

User = get_user_model()

gender_choices = (
    ("male", "Male"),
    ("female", "Female"),
    ("none", "Not Specify"),
)
# Create your models here.

class ChitChat(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="Synthia")
    bot_type = models.CharField(max_length=255, default="ai-assistant")
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=255, default="none", choices=gender_choices)
    prompt = models.TextField(default="The following is a conversation with an AI assistant whose name is Synthia. The assistant is helpful, creative, clever, and very friendly")
    
    def __str__(self):
        return self.name+ "/" +self.user.first_name
    