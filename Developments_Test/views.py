import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
#, render_to_response
from django.contrib import messages
from django.db.models import Q

from .forms import UserForm,UserRegistrationForm
from .models import Users
from Developments_Test import services
import requests
from django.db.models import Avg
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext


def index(request):
    user = request.user
    if user.is_active:
        if Users.objects.filter(user=user):
            context = {
                'users': 'users',
            }
        return render(request, 'Developments_Tests/login.html', context)
    else:
        return render(request, 'Developments_Tests/login.html')

#Teacher Registration
def register(request):
    form = UserForm(request.POST or None)
    user_reg_form = UserRegistrationForm(request.POST or None)
    if form.is_valid() and user_reg_form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        user.set_password(password)
        user.save()

        profile = user_reg_form.save(commit=False)
        profile.user = user
        profile.save()

        messages.info(request, 'Registration Successfull')
        return render(request, 'Developments_Tests/login.html')
    context = {
        "form": form,
        "user_reg_form": user_reg_form,
    }
    return render(request, 'Developments_Tests/registration.html', context)

@login_required
def home(request):
    user = request.user
    if user.is_active:
        if Users.objects.filter(user=user):
            # info_list = services.get_info()
            info_list = requests.get('https://jsonplaceholder.typicode.com/posts').json()
            return render(request, 'Developments_Tests/home.html', {'info_list': info_list})
        else:
            return render(request, 'Developments_Tests/login.html')

@login_required
def otherpost(request):
    user = request.user
    if user.is_active:
        if Users.objects.filter(user=user):
            # info_list = services.get_info()
            info_list = requests.get('https://jsonplaceholder.typicode.com/posts').json()
            return render(request, 'Developments_Tests/other-post.html', {'info_list': info_list})
        else:
            return render(request, 'Developments_Tests/login.html')

def postdetails(request, id):
    user = request.user
    if user.is_active:
        if Users.objects.filter(user=user):
            # info_list = services.get_info()
            info_list1 = requests.get('https://jsonplaceholder.typicode.com/posts/'+id+'/').json()
            info_list2 = requests.get('https://jsonplaceholder.typicode.com/posts/'+id+'/comments/').json()
            context = {
                "info_list1": info_list1,
                "info_list2": info_list2,
            }
            return render(request, 'Developments_Tests/post-details.html', context)
        else:
            return render(request, 'Developments_Tests/login.html')

#User Login
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                if Users.objects.filter(user=user):
                    login(request, user)
                    info_list = requests.get('https://jsonplaceholder.typicode.com/posts').json()
                    return render(request, 'Developments_Tests/home.html', {'info_list': info_list})
                else:
                    return render(request, 'Developments_Tests/login.html', {'error_message': 'Invalid login'})
            else:
                context = {
                    'users': 'users',
                }
                return render(request, 'Developments_Tests/login.html', context)
        else:
            return render(request, 'Developments_Tests/login.html', {'error_message': 'Invalid login'})
    else:
        user = request.user
        if user.is_active:
            if Users.objects.filter(user=user):
                context = {
                    'users': 'users',
                }
            return render(request, 'Developments_Tests/login.html', context)
        else:
            return render(request, 'Developments_Tests/login.html')

def logout_user(request):
    if request.method == "POST":
        logout(request)
        form = UserForm(request.POST or None)
        context = {
            "form": form,
        }
        return render(request, 'Developments_Tests/login.html', context)
    else:
        user = request.user
        if user.is_active:
            if Users.objects.filter(user=user):
                context = {
                    'users': 'users',
                }
            return render(request, 'Developments_Tests/login.html', context)
        else:
            return render(request, 'Developments_Tests/login.html')

