from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
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
    places = Place.objects.filter(user_id=request.user)
    context = {'places': places}
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

def stream_video(request):
    cameras = Camera.objects.filter(user_id=request.user)
    camera = IpCamera(request, cameras[3].pk)
    print(camera.camera)
    print(camera.url)
    return StreamingHttpResponse(generate_frames(camera), content_type='multipart/x-mixed-replace; boundary=frame')

@login_required(login_url="/login/")
def reports(request):
    return render(request, 'cabinet/reports.html')

@login_required(login_url="/login/")
def journal(request):
    violations = Violation.objects.all()
    context = {'violations': violations}
    return render(request, 'cabinet/journal.html', context)

@login_required(login_url="/login/")
def statistics(request):
    return render(request, 'cabinet/statistics.html')

def generate_frames(camera):
    capture = cv2.VideoCapture(camera.url)
    print(capture.isOpened())
    while capture.isOpened():
        ret, frame = capture.read()
        img = cv2.imdecode(frame, 1)
        resize = cv2.resize(img, (640, 480), interpolation=cv2.INTER_LINEAR)
        _, jpeg = cv2.imencode('.jpg', resize)
        frame = jpeg.tobytes()
        yield b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
