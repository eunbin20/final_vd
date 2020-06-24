from django.contrib.auth.models import User
from flask import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.template import RequestContext
from django.contrib.auth import login as auth_login

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            auth_login(request, user)
            return redirect('/')
        else:
            return HttpResponse('로그인 실패. 다시 시도 해보세요.')
    else:
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(**form.cleaned_data)
            auth_login(request, user)
        return redirect('/')
    else:
        form = UserForm()
    return render(request, 'accounts/signup.html', {'form': form})


# def signup(request):
#     if request.method == "POST":
#         if request.POST['password1'] == request.POST['password2']:
#             user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
#             auth.login(request, user)
#         return redirect('home')
#     return render(request, 'accounts/signup.html')


# def login(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user=auth.authenticate(request, username=username, password=password)
#         if user is not None:
#             auth.login(request, user)
#             return redirect('show')
#         else:
#             return render(request, 'accounts/login.html', {'error': 'username or password is incorrect.'})
#     else:
#         return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')



