from django.db import models
from django.conf import settings

class AppUser(models.Model): 
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
    )

    def __str__(self):
        return self.user.username

class MusicFile(models.Model): 
    title = models.CharField(default="file", max_length=50, null=False)
    description = models.CharField(max_length=2500)
    creation_date = models.DateField(null=True)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)

    def __str__(self): 
        return "Name: " + self.name
