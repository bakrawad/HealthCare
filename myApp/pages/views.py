from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.shortcuts import HttpResponse
from django.contrib import messages
from . import models
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
import bcrypt
import re

def success(request):
    if 'user' in request.session:
        context = request.session['user']
        return render(request,"success.html",context)
    else:
        return HttpResponse("You are not logged in")
    
def index(request):
    return render(request,"login.html")

def create_user(fname, lname, email, phone, passwd):
    salt = bcrypt.gensalt()
    enc_pass = bcrypt.hashpw(passwd.encode(), salt).decode()
    new_user = models.Users.objects.create(
        first_name=fname,
        last_name=lname,
        email=email,
        phone=phone,
        password=enc_pass
    )
    return new_user

def register(request):
    if request.method == "POST":
        errors = models.Users.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/zo/register')
        else:
            first_name1 = request.POST['fname']
            last_name1 = request.POST['lname']
            phone = request.POST['phone']
            email1 = request.POST['email']
            password = request.POST['password']
            password_confirmation=request.Post['password_confirmation']
            if password != password_confirmation:
                messages.error(request, "Passwords do not match.")
                return redirect('/zo/register')

            
            user = create_user(first_name1, last_name1,phone, email1, password,password_confirmation)
            print('Created3')
            request.session['fname'] = user.first_name
            request.session['lname'] = user.last_name
            request.session['email'] = user.last_namerequest.session['first_name'] = user.first_name
            print('Created4')

    return render(request, 'register.html')

def login(request):
    if request.method == "POST":
        email = request.POST['myemail']
        password = request.POST['mypassword']
        user = models.Users.objects.filter(email=email).first()
        if user and bcrypt.checkpw(password.encode(), user.password.encode()):
            request.session['user'] = {
                'fname': user.first_name,
                'lname': user.last_name,
                'email': user.email
            }
            return redirect('/zo/success')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('/zo/login')
    
    return render(request, 'login.html')


def Success1(request):
    if 'fname' not in request.session:
        return redirect('/zo/login')
    
    context = {
        'fname': request.session['fname'],
        'lname': request.session['lname'],
    }
    return render(request, "success.html", context)
