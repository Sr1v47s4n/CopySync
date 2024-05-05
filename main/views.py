from django.shortcuts import render,redirect
from .models import Paste
import random,string
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def home(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            print(request.POST)
            content = request.POST.get("content")
            type = request.POST.get("type")
            paste = Paste(content=content, type=type, url=url_gen(),user=request.user)
            paste.save()
            messages.info(request, f'Your paste has been created successfully! {paste.url}')
            return redirect(f"view/{paste.url}")
        return render(request, "home.html")
    else:
        if request.method == "POST":
            print(request.POST)
            content = request.POST.get("content")
            paste = Paste(content=content, url=url_gen())
            paste.save()
            messages.info(
                request,
                f'Your paste has been created successfully! {paste.url}',
            )
            return redirect(f"view/{paste.url}")
    return render(request, "home.html")

def url_gen():
    return "".join(random.choices(string.ascii_letters + string.digits+string.hexdigits, k=6))

def paste(request, url):
    paste = Paste.objects.get(url=url)
    if paste.type != "public":
        if not request.user.is_authenticated:
            messages.info(request, f"Please login to view this paste! {url}")
            return redirect("home")
        else:
            if request.user != paste.user:
                messages.info(request, f"You are not authorized to view this paste! {url}")
                return redirect("home")
        if paste.expiration_date < timezone.now():
            paste.delete()
            messages.info(request, f"This paste has expired! {url}")
            return redirect("home")
        return render(request, "paste.html", {"paste": paste})
    if paste.expiration_date < timezone.now():
        paste.delete()
        messages.info(request, f"This paste has expired!{url}")
        return redirect("home")
    return render(request, "paste.html", {"paste": paste})

def view_paste(request):
    if request.user.is_authenticated:
        pastes = Paste.objects.filter(user=request.user)
        print(pastes)
        return render(request, "view_paste.html", {"pastes": pastes})
    else:
        messages.info(request, "Please login to view your pastes!")
        return redirect("home")

def delete_paste(request, url):
    paste = Paste.objects.get(url=url)
    if paste.type != "public":
        if request.user == paste.user:
            paste.delete()
            messages.info(request, f"Paste deleted successfully! {url}")
            return redirect("view_paste")
        else:
            messages.info(request, f"You are not authorized to delete this paste! {url}")
            return redirect("home")
    else:
        paste.delete()
        messages.info(request, f"Paste deleted successfully! {url}")
        return redirect("home")


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, f"Welcome back, {username}!")
            return redirect("home")
        else:
            messages.info(request, "Invalid credentials!")
            return redirect("login")
    return render(request, "auth/login.html")

def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.info(request, f"Account created for {username}!")
        return redirect("login")
    return render(request, "auth/register.html")

def logout_user(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home")
