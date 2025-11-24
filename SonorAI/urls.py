"""
URL configuration for SonorAI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path(route="admin/", view=admin.site.urls),
    path(route="", view=views.homepage_view, name="homepage"), # type: ignore
    path(route="logout/", view=views.logout_request, name="logout"), 
    path(route="login/", view=views.login_request, name="login"), 
    path(route="register/", view=views.register_request, name="register"), # type: ignore
    path(route="upload_audio/", view=views.upload_audio, name="upload_audio"), 
    path(route="download/<int:pk>", view=views.download_musicxml, name="download_musicxml"), # type: ignore
    path(route="myfiles/", view=views.myfiles_view, name="myfiles"), # type: ignore
    path(route="myfiles/delete/<int:pk>", view=views.delete_myfiles, name="delete_myfiles"), # type: ignore
    path(route="myfiles/rename/<int:pk>", view=views.rename_myfiles, name="rename_myfiles"), # type: ignore
    
]
