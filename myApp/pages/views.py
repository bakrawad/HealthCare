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

def create_user(fname, lname, email, passwd):
    salt = bcrypt.gensalt()
    enc_pass = bcrypt.hashpw(passwd.encode(), salt).decode()
    new_user = models.Users.objects.create(
        first_name=fname,
        last_name=lname,
        email=email,
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
            
            user = create_user(first_name1, last_name1,phone, email1, password,password_confirmation)
            print('Created3')
            request.session['fname'] = user.first_name
            request.session['lname'] = user.last_name
            request.session['phone'] = user.phone
            request.session['email'] = user.last_namerequest.session['first_name'] = user.first_name
            request.session['password'] = user.password
            request.session['password_confirmation'] = user.password_confirmation

            print('Created4')

    return render(request, 'register.html')

def login(request):
    if request.method == "POST":
        email = request.POST['myemail']
        password = request.POST['mypassword']
        user = models.Users.objects.filter(email=email).first()
        if user and bcrypt.checkpw(password.encode(), user.password.encode()):
            request.session['fname'] = user.first_name
            request.session['lname'] = user.last_name
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
