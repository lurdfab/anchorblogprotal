from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "first_name", "last_name", "email", "date_joined", "updated_at")

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "gender", "address", "phone_number")


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)


