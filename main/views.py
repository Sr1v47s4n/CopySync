from django.shortcuts import render,redirect
from .models import Paste, File
import random,string
import os
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout

def home(request):
    try:
        if request.user.is_authenticated:
            if request.method == "POST":
                content = request.POST.get("content")
                type = request.POST.get("type")
                if content == "":
                    messages.error(request, "Please enter some content!")
                    return redirect("home")
                paste = Paste(content=content, type=type, url=url_gen(),user=request.user)
                paste.save()
                messages.info(request, f'Your paste has been created successfully! {paste.url}')
                return redirect(f"view/{paste.url}")
            return render(request, "home.html")
        else:
            if request.method == "POST":
                content = request.POST.get("content")
                if content == "":
                    messages.error(request, "Please enter some content!")
                    return redirect("home")
                paste = Paste(content=content, url=url_gen())
                paste.save()
                messages.info(
                    request,
                    f'Your paste has been created successfully! {paste.url}',
                )
                return redirect(f"view/{paste.url}")
        return render(request, "home.html")
    except Exception as e:
        messages.error(request, f"Error while creating your paste")
        return redirect("home")

def file(request):
    try:
        if request.user.is_authenticated:
            if request.method == "POST" and request.FILES.get("file"):
                content = request.FILES["file"]
                if content.size > 20 * 1024 * 1024:
                    messages.error(
                        request,
                        "File size limit exceeded! Please upload a file less than 20MB.",
                    )
                    return redirect("file")
                file_type = request.POST.get("type")
                if not file_type:
                    messages.error(request, "Please select a file type!")
                    return redirect("file")
                file = File(
                    content=content, url=url_gen(), type=file_type, user=request.user
                )
                file.save()
                messages.info(request, f"File uploaded successfully! {file.url}")
                return redirect("view_file", url=file.url)
            return render(request, "file.html")
        else:
            if request.method == "POST" and request.FILES.get("file"):
                content = request.FILES["file"]
                if content.size > 20 * 1024 * 1024:
                    messages.error(
                        request,
                        "File size limit exceeded! Please upload a file less than 20MB.",
                    )
                    return redirect("file")
                
                file = File(content=content, url=url_gen(), type=file_type)
                file.save()
                messages.info(request, f"File uploaded successfully! {file.url}")
                return redirect("view_file", url=file.url)
            return render(request, "file.html")
    except Exception as e:
        messages.error(request, f"Error while uploading your file")
        return redirect("file")


def view_file(request, url):
    try:
        file = File.objects.get(url=url)
        if file.type != "public":
            if not request.user.is_authenticated:
                messages.info(request, f"Please login to view this file! {url}")
                return redirect("home")
            else:
                if request.user != file.user:
                    messages.info(request, f"You are not authorized to view this file! {url}")
                    return redirect("home")
            if file.expiration_date < timezone.now():
                file.delete()
                os.remove(file.content.path)
                messages.info(request, f"This file has expired! {url}")
                return redirect("home")
            return render(request, "view_file.html", {"file": file})
        if file.expiration_date < timezone.now():
            file.delete()
            
            os.remove(file.content.path)

            messages.info(request, f"This file has expired! {url}")
            return redirect("home")

        return render(request, "view_file.html", {"file": file})
    except:
        messages.error(request, "File does not exist!")
        return redirect("home")


def url_gen():
    if Paste.objects.filter(url=url_gen).exists() or File.objects.filter(url=url_gen).exists():
        return url_gen()
    return "".join(random.choices(string.ascii_letters + string.digits+string.hexdigits, k=6))

def paste(request, url):
    try:
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
    except:
        messages.error(request, "Paste does not exist!")
        return redirect("home")
def view_paste(request):
    try:
        if request.user.is_authenticated:
            pastes = Paste.objects.filter(user=request.user)
            print(pastes)
            return render(request, "view_paste.html", {"pastes": pastes})
        else:
            messages.info(request, "Please login to view your pastes!")
            return redirect("home")
    except Exception as e:
        messages.error(request, "Error while fetching your pastes!")
        return redirect("home")

def delete_paste(request, url):
    try:
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
    except Paste.DoesNotExist:
        messages.error(request, "Paste does not exist!")
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
    try:
        if request.method == "POST":
            username = request.POST.get("username")
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already exists!")
                return redirect("register")
            password = request.POST.get("password")
            user = User.objects.create_user(username=username, password=password)
            user.save()
            messages.info(request, f"Account created for {username}!")
            return redirect("login")
        return render(request, "auth/register.html")
    except Exception as e:
        messages.error(request, "Error while creating your account!")
        return redirect("register")

def logout_user(request):
    if not request.user.is_authenticated:
        messages.info(request, "You are not logged in!")
        return redirect("login")
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home")

def delete_file(request, url):
    try:
        file = File.objects.get(url=url)
        if file.type != "public":
            if request.user == file.user:
                file.delete()
                os.remove(file.content.path)
                messages.info(request, f"File deleted successfully! {url}")
                return redirect("home")
            else:
                messages.info(request, f"You are not authorized to delete this file! {url}")
                return redirect("home")
        else:
            file.delete()
            os.remove(file.content.path)
            messages.info(request, f"File deleted successfully! {url}")
            return redirect("home")
    except File.DoesNotExist:
        messages.error(request, "File does not exist!")
        return redirect("home")
    except Exception as e:
        messages.error(request, f"File deleted successfully! {url}")
        return redirect("home")

def view_files(request):
    try:
        if request.user.is_authenticated:
            files = File.objects.filter(user=request.user)
            return render(request, "view_files.html", {"files": files})
        else:
            messages.info(request, "Please login to view your files!")
            return redirect("home")
        
    except Exception as e:
        messages.error(request, "Error while fetching your files!")
        return redirect("home")

def about(request):
    return render(request, "about.html")


def error_404(request, exception):
    messages.error(request, "Page not found!")
    return redirect("home")


def error_500(request):
    messages.error(request, "Something went wrong!")
    return redirect("home")
