from django.contrib import admin
from .models import *


class VideoAdmin(admin.ModelAdmin):
    list_display=( "user", "title", "upload_date")

class MusicAdmin(admin.ModelAdmin):
    list_display=("user", "title", "upload_date")


admin.site.register(Video, VideoAdmin)
admin.site.register(Music, MusicAdmin)
