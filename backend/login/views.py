import re
import hashlib
from django.shortcuts import redirect, render
from . import models

# Create your views here.


def login(request):
    if request.session.get('is_login', None):
        username=request.session['user_name']
        return render(request, 'Logout.html', locals())

    if request.method == 'POST':
        login_form = models.UserForm(request.POST)
        message = "All fields must be filled!"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/')
                else:
                    message = "Wrong password!"
            except:
                message = "User does not exist!"
        return render(request, 'Login.html', locals())

    login_form = models.UserForm()
    return render(request, 'Login.html', locals())


def register(request):
    if request.session.get('is_login', None):
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
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = 'User already exists, please select a new user name.'
                    return render(request, 'Register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = 'This email address has already been registered, please use another email address.'
                    return render(request, 'Register.html', locals())

                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.save()
                return redirect('/login/')

    register_form = models.RegisterForm()
    return render(request, 'Register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    request.session.flush()
    return redirect('/login/')


def hash_code(s, salt='finmaster'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()
