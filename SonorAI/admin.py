from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import MusicFile

# Inline class to appear in UserFileAdmin
class MusicFileInline(admin.TabularInline): 
    model = MusicFile
    fields = ["title", "creation_date", "musicxml"]
    readonly_fields = ["creation_date"]
    extra = 0 # No extra sections
    can_delete = True # Admin may delete file

# Admin classes
class UserFileAdmin(UserAdmin): 
    inlines = [MusicFileInline]

class MusicFileAdmin(admin.ModelAdmin):
    list_display = ["title", "creation_date", "user", "musicxml"]
    list_filter = ["user"]

# Registrations
admin.site.unregister(User)
admin.site.register(User, UserFileAdmin)
admin.site.register(MusicFile, MusicFileAdmin)
