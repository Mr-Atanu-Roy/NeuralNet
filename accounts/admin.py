from django.contrib import admin
from .models import *
from core.models import ChitChat
# Register your models here.

class ChitChatInline(admin.StackedInline):
    model = ChitChat
    extra = 0
    
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'is_verified', 'is_staff', 'last_login')
    fieldsets = [
        ("User Details", {
            "fields": (
                ['email', 'password', 'first_name', 'last_name']
            ),
        }),
        ("More Details", {
            "fields": (
                ['is_verified', 'date_joined', 'last_login']
            ), 'classes': ['collapse']
        }),
        ("Permissions", {
            "fields": (
                ['is_staff', 'is_superuser', 'is_active', 'user_permissions', 'groups']
            ),
        }),
    ]
    
    inlines = [ChitChatInline]
    
    search_fields = ["email", "first_name", "last_name", "is_verified"]

class OTPAdmin(admin.ModelAdmin):
    list_display = ("auth_token", "is_expired", "purpose", "created_at")
    fieldsets = [
        ("OTP Details", {
            "fields": (
                ['auth_token', 'user', 'purpose', 'is_expired']
            ),
        }),
    ]
    
    search_fields = ['user', 'purpose']

admin.site.register(User, UserAdmin)
admin.site.register(OTP, OTPAdmin)