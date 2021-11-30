from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['date_joined']
        verbose_name = 'user'
        verbose_name_plural = 'user'

class UserForm(forms.Form):
    username=forms.CharField(label='Username:',max_length=128,widget=forms.TextInput(attrs={'class':'name-input'}))
    password=forms.CharField(label='Password:',max_length=256,widget=forms.PasswordInput(attrs={'class':'pwd-input'}))

class RegisterForm(forms.Form):
    username=forms.CharField(label='Username:',max_length=128,widget=forms.TextInput(attrs={'class':'name-input'}))
    password1=forms.CharField(label='Password:',max_length=256,widget=forms.PasswordInput(attrs={'class':'pwd-input'}))
    password2=forms.CharField(label='Confirm password:',max_length=256,widget=forms.PasswordInput(attrs={'class':'pwd-input'}))
    email=forms.EmailField(label='Email address:',widget=forms.EmailInput(attrs={'class':'email-input'}))