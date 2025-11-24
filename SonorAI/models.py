from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class MusicFile(models.Model): 
    title = models.CharField(default="file", max_length=50, null=False)
    creation_date = models.DateField(auto_now_add=True)
    musicxml = models.TextField() # Store entire file
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self): 
        return self.user.username+"-"+self.title
