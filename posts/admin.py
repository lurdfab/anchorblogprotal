from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "category")


admin.site.register(Post, PostAdmin)
