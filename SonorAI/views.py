from .models import *
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic, View
from django.contrib.auth import login, logout, authenticate
from . import aiapp
from collections import defaultdict
import logging
import os

# Start logging
logger = logging.getLogger(__name__)

# Authentication
def logout_request(request):
    logout(request)
    return redirect('homepage')

def login_request(request):
    context = {}
    # Check method
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']

        # Validate credentials
        user = authenticate(username=username, password=password)
        
        if user: # Valid case
            login(request, user)
            return redirect('homepage')
        
        else: # Invalid case
            context["message"] = "Invalid username or password."
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

        # Check duplicates
        if User.objects.filter(username=username).exists():
            context["message"] = "Username already exists."
            return render(request, "register.html", context)

        # Generate new user
        else:
            user = User.objects.create_user(
                username=username, 
                first_name=first_name, 
                last_name=last_name,
                password=password,
                email=username
            )
            # Login
            login(request, user)
            return redirect("homepage")
        
    else: # Incorrect method
        return render(request, 'register.html', context)

def upload_audio(request): 
    context = {}
    # Check method
    if request.method == 'POST': 
        audio_file = request.FILES.get('audio_file')
        
        # Check upload parameters
        if not audio_file: 
            return HttpResponse("No file uploaded.")
        if not audio_file.name.lower().endswith(".wav"): 
            return HttpResponse("Invalid file type.")
        
        input_path = "temp.wav"

        # Cleanup old AI analysis input (if exists)
        if os.path.exists(input_path): 
            os.remove(input_path)

        # Cleanup old AI analysis output (if exists)
        if os.path.exists("out.musicxml"): 
            os.remove("out.musicxml")

        # Temporarily store the file
        with open(input_path, "wb") as file: 
            for chunk in audio_file.chunks(): 
                file.write(chunk)

        # Run AI analysis (stores output as out.musicxml in current path)
        aiapp.AudioAnalysis.audio_analysis(audio_file=input_path, title=audio_file.name.replace(".wav", ""))

        # Retrieve results
        if not os.path.exists("out.musicxml"): 
            context["message"] = "Audio analysis failed."
            return render(request, "index.html", context)
        
        with open("out.musicxml", "r", encoding="utf-8") as file: 
            musicxml = file.read()
        
        # Cleanup AI analysis input
        if os.path.exists(input_path): 
            os.remove(input_path)
        
        # Cleanup AI analysis output
        if os.path.exists("out.musicxml"): 
            os.remove("out.musicxml")

        # Store results in database if the user is signed in
        if request.user.is_authenticated: 
            file = MusicFile.objects.create(
                title = audio_file.name, 
                musicxml=musicxml, 
                user = request.user
            )
            context = {
                "musicxml": musicxml, 
                "message": "MusicXML stored in My Files.", 
                "pk": file.pk # For download button
            }

        # Return contents if the user is not signed in
        else: 
            context = {
                "musicxml": musicxml, 
                "message": "MusicXML not stored, sign in to store and download file."
            }
        
        return render(request, "index.html", context)
    
    else: # Incorrect method
        return render(request, "index.html", context)
        
def download_musicxml(request, pk): 
    # Check method
    if request.method == 'GET': 
        file = get_object_or_404(MusicFile, pk=pk, user=request.user)
        response = HttpResponse(file.musicxml, content_type="application/xml")
        response['Content-Disposition'] = f'attachment; filename="{file.title}.musicxml"'
        return response

def delete_myfiles(request, pk): 
    file = get_object_or_404(MusicFile, pk=pk, user=request.user)
    file.delete()
    return redirect("myfiles")

def rename_myfiles(request, pk): 
    file = get_object_or_404(MusicFile, pk=pk, user=request.user)
    name = request.POST.get("name", "").strip()
    if name: 
        file.title = name
        file.save()
    return redirect("myfiles")

# Pages
def homepage_view(request):
    context = {}
    if request.method in ("GET", "HEAD"):
        return render(request, "index.html", context)
    # fall back to same page for any other method
    return render(request, "index.html", context)

def myfiles_view(request): 
    context = {}
    # Check method
    if request.method == 'GET': 
        # Send user to login page if not logged in
        if not request.user.is_authenticated: 
            return redirect("login")
        
        # Get matching MusicXML files
        files = MusicFile.objects.filter(user=request.user)
        context["files"] = files
        return render(request, "myfiles.html", context)
