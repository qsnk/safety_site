from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from ui.forms import LoginForm, SignupForm


def index(request):
    return render(request, 'ui/index.html')

def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                if password1 == password2:
                    form.save()
                return redirect('/login/')

    form = SignupForm()
    context = {'form': form}
    return render(request, 'ui/signup.html', context)


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('/cabinet/')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return redirect('/cabinet/')
            else:
                messages.error(request, "Неверное имя пользователя или пароль!")
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'ui/login.html', context)

