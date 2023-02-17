from django.contrib import admin
from .models import *

# Register your models here.

class ChitChatAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'bot_type', 'created_at')
    fieldsets = [
        ("User", {
            "fields": (
                ['user']
            ),
        }), 
        ("Bot Details", {
            "fields": (
                ['name', 'age', 'gender', 'prompt']
            ),
        }),
    ]
    
    search_fields = ["name", "age", "user"]

admin.site.register(ChitChat, ChitChatAdmin)