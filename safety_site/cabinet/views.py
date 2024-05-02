from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from cabinet.forms import AddCameraForm, AddPlaceForm, ShowPlaceForm
from cabinet.models import Camera, Place


# Create your views here.
@login_required(login_url="/login/")
def index(request):
    user = request.user
    context = {"user": user}
    return render(request, 'cabinet/index.html', context)

@login_required(login_url="/login/")
def add_cameras(request):
    if request.method == "POST":
        form = AddCameraForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            url = form.cleaned_data["url"]
            user_id = request.user
            camera = Camera(name=name, url=url, user_id=user_id)
            camera.save()
        else:
            messages.error(request, "Invalid data!")
    else:
        form = AddCameraForm
    cameras = Camera.objects.all()
    context = {'form': form, "cameras": cameras}
    return render(request, 'cabinet/add_cameras.html', context)

@login_required(login_url="/login/")
def add_places(request):
    if request.method == "POST":
        form = AddPlaceForm(request.POST, user_id=request.user)
        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            camera_id = form.cleaned_data["camera_id"]
            user_id = request.user
            place = Place(name=name, description=description, camera_id=camera_id, user_id=user_id)
            place.save()
        else:
            messages.error(request, "Invalid data!")
    else:
        form = AddPlaceForm(user_id=request.user)
    places = Place.objects.all()
    context = {'form': form, 'places': places}
    return render(request, 'cabinet/add_place.html', context)

@login_required(login_url="/login/")
def watch_site(request):
    if request.method == "POST":
        form = ShowPlaceForm(request.POST, user_id=request.user)
    else:
        form = ShowPlaceForm(user_id=request.user)
    context = {'form': form}
    return render(request, 'cabinet/watch_site.html', context)

@login_required(login_url="/login/")
def reports(request):
    return render(request, 'cabinet/reports.html')

@login_required(login_url="/login/")
def journal(request):
    return render(request, 'cabinet/journal.html')

@login_required(login_url="/login/")
def statistics(request):
    return render(request, 'cabinet/statistics.html')
