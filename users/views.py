from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import UserRegisterForm

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автовход после регистрации
            messages.success(request, "Вы успешно зарегистрировались!")
            return redirect("home")  # Измените на свою страницу
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Неверные данные!")
    return render(request, "users/login.html")

def user_logout(request):
    logout(request)
    return redirect("home")
