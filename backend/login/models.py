from django.db import models
from django import forms
from django.forms.forms import Form

# Create your models here.

class User(models.Model):
    """
    User sheet.
    """
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
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