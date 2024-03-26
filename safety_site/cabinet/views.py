from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'cabinet/index.html')

def cameras(request):
    return render(request, 'cabinet/cameras.html')

