from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from ui.forms import LoginForm

# Create your views here.

def index(request):
    return render(request, 'ui/index.html')

def sign_in(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return redirect('/cabinet/')
            else:
                messages.error(request, "Wrong username or password")
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'ui/login.html', context)

