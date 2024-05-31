from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.cache import cache
from django.core.paginator import Paginator
from django.http.response import StreamingHttpResponse, HttpResponse
from cabinet.forms import AddCameraForm, AddPlaceForm, ShowPlaceForm
from cabinet.models import Camera, Place, Violation
from cabinet.camera import IpCamera
import cv2

# Create your views here.
@login_required(login_url="/login/")
def index(request):
    user = request.user
    username = user.username
    first_name = user.first_name
    last_name = user.last_name
    email = user.email
    date_joined = user.date_joined
    is_active = user.is_active
    user_info = [username, email, date_joined]
    context = {
        'user': user,
        'user_info': user_info,
        'username': username,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'date_joined': date_joined
    }
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
    paginator = Paginator(cameras, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'form': form, "cameras": cameras, "page": page}
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
    paginator = Paginator(places, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'form': form, 'places': places, 'page': page}
    return render(request, 'cabinet/add_place.html', context)

@login_required(login_url="/login/")
def watch_site(request):
    places = Place.objects.filter(user_id=request.user)
    if request.method == "POST":
        sites_id = request.POST.getlist("checkboxes")
        all_sites = Place.objects.all()
        sites_names = []
        for id in sites_id:
            sites_names.append(all_sites.get(pk=id))
        sites = {key:value for key, value in zip(sites_id, sites_names)}
        cache.set('sites', sites, 60 * 60 * 24)
        print(sites)
    else:
        sites_cache = cache.get('sites')
        if sites_cache is not None:
            sites = sites_cache
        else:
            sites = None
        cache.set('sites', sites, 60 * 60)
    context = {'places': places, 'sites': sites}
    return render(request, 'cabinet/watch_site.html', context)

def watch_site_add(request):
    for k, v in request.POST.items():
        places = Place.objects.filter(pk=id)
        print(k, v)
    return HttpResponse(
        status=204,
        headers={
            "showMessage": "Places shown"
    })

def watch_site_start(request):
    pass

def watch_site_stop(request):
    cache.set('sites', None, 60 * 60)
    cv2.VideoCapture().release()
    return HttpResponse(
        status=204,
        headers={
            "showMessage": "Processing stopped"
        })

def stream_video(request):
    sites_cached = cache.get('sites')
    if sites_cached is not None:
        index = int(list(sites_cached.keys())[0])
        chosen_camera = Place.objects.get(pk=index).camera_id
        url = chosen_camera.url
        camera = IpCamera(url)
        return StreamingHttpResponse(generate_frames(request, camera), content_type='multipart/x-mixed-replace; boundary=frame')

@login_required(login_url="/login/")
def reports(request):
    return render(request, 'cabinet/reports.html')

@login_required(login_url="/login/")
def journal(request):
    violations = Violation.objects.all()
    paginator = Paginator(violations, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'violations': violations, 'page': page}
    return render(request, 'cabinet/journal.html', context)

@login_required(login_url="/login/")
def statistics(request):
    return render(request, 'cabinet/statistics.html')

def generate_frames(request, camera):
    while camera.capture.isOpened():
        frame = camera.get_frame(request)
        yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')