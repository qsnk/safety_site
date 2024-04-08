from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'cabinet/index.html')

def add_cameras(request):
    return render(request, 'cabinet/add_cameras.html')

def watch_site(request):
    return render(request, 'cabinet/watch_site.html')

def reports(request):
    return render(request, 'cabinet/reports.html')

def journal(request):
    return render(request, 'cabinet/journal.html')

def statistics(request):
    return render(request, 'cabinet/statistics.html')
