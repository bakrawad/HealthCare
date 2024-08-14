from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from . import models
def index(request):
      pass
   
def login(request):
    return render(request, 'pages/login.html')


def register(request):
   
            return render(request, 'pages/register.html')

def addPat(request):
      return render(request,'pages/addPat.html')


def dash(request):
   return render(request,'pages/dash.html')