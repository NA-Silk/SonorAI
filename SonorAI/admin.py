from django.contrib import admin
from .models import *

class MusicFileAdmin(admin.ModelAdmin):
    list_display = ["title", "musicxml", "creation_date", "user"]

#admin.site.register(AppUser)
admin.site.register(MusicFile, MusicFileAdmin)
