from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404
from django.urls import reverse
from django.views import generic, View
from collections import defaultdict
from django.contrib.auth import login, logout, authenticate
import logging

# Start logging
logger = logging.getLogger(__name__)

# Authentication
def logout_request(request):
    logout(request)
    return redirect('home_page')

def login_request(request):
    context = {}
    # Check method
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']

        # Validate credentials
        user = authenticate(username=username, password=password)
        if user is not None: # Valid case
            login(request, user)
            return redirect('home_page')
        
        else: # Invalid case
            return render(request, 'login.html', context)
    
    else: # Incorrect method
        return render(request, 'login.html', context)

def register_request(request):
    context = {}
    # Check method
    if request.method == 'GET':
        return render(request, 'register.html', context)
    
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False

        try: # Check if duplicate
            User.objects.get(username=username)
            user_exist = True
        except: # Log new user
            logger.debug("{} is new user".format(username))

        # Generate new user
        if not user_exist:
            user = User.objects.create_user(
                username=username, 
                first_name=first_name, 
                last_name=last_name,
                password=password
            )

            # Login
            login(request, user)
            return redirect("home_page")
        
        else: # Incorrect method
            return render(request, 'register.html', context)

# Pages
def home_page_view(request): 
    context = {}
    if request.method == 'GET': 
        return render(request, "index.html", context)

class MyFilesView(generic.DetailView): 
    model = MusicFile
    template_name = "myfiles.html"
