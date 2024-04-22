from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from cabinet.forms import AddCameraForm
from cabinet.models import Camera


# Create your views here.
def index(request):
    return render(request, 'cabinet/index.html')

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
            print(form.errors)
            messages.error(request, "Invalid data!")
    else:
        form = AddCameraForm
    cameras = Camera.objects.all()
    context = {'form': form, "cameras": cameras}
    return render(request, 'cabinet/add_cameras.html', context)

def watch_site(request):
    return render(request, 'cabinet/watch_site.html')

def reports(request):
    return render(request, 'cabinet/reports.html')

def journal(request):
    return render(request, 'cabinet/journal.html')

def statistics(request):
    return render(request, 'cabinet/statistics.html')
