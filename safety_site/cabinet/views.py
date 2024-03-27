from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'cabinet/index.html')

def cameras(request):
    return render(request, 'cabinet/cameras.html')

def reports(request):
    return render(request, 'cabinet/reports.html')

def journal(request):
    return render(request, 'cabinet/journal.html')

def statistics(request):
    return render(request, 'cabinet/statistics.html')
