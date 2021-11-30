import re
import hashlib
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from . import models

# Create your views here.


def login(request):
    if request.user.is_authenticated:
        username = request.user.username
        return render(request, 'Logout.html', locals())

    if request.method == 'POST':
        login_form = models.UserForm(request.POST)
        message = "All fields must be filled!"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=hash_code(password))
            if user is not None:
                auth_login(request,user)
                return redirect('/')
            else:
                message="Invalid login. Please check your inputs."
        return render(request, 'Login.html', locals())

    login_form = models.UserForm()
    return render(request, 'Login.html', locals())


def register(request):
    if request.user.is_authenticated:
        return redirect('/login/')

    if request.method == 'POST':
        register_form = models.RegisterForm(request.POST)
        message = 'All fields must be filled!'
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            if password1 != password2:
                message = 'Two different passwords entered!'
                return render(request, 'Register.html', locals())
            else:
                same_name_user = models.User.objects.filter(username=username)
                if same_name_user:
                    message = 'User already exists, please select a new user name.'
                    return render(request, 'Register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = 'This email address has already been registered, please use another email address.'
                    return render(request, 'Register.html', locals())

                new_user = models.User.objects.create_user(username=username,password=hash_code(password1),email=email)
                return redirect('/login/')

    register_form = models.RegisterForm()
    return render(request, 'Register.html', locals())


def logout(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    auth_logout(request)
    return redirect('/login/')


def hash_code(s, salt='finmaster'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()
