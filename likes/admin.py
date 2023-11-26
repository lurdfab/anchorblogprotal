from django.contrib import admin
from .models import *


# class LikeAdmin(admin.ModelAdmin):
#     list_display = ('liked_by',)

admin.site.register(Like,)
