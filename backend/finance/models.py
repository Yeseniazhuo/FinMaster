from django.db import models
from django.db.models.base import Model
from django.forms import ModelForm
from login.models import User

# Create your models here.

INTERVAL_CHOICES = [('1day','1day'), ('1hour', '1hour'), ('5mins', '5mins'), ('1min', '1min')]

class Settings(models.Model):
    symbol1 = models.CharField(max_length=20, default='AAPL')
    interval1 = models.CharField(max_length=5, choices=INTERVAL_CHOICES, default='1day')
    symbol2 = models.CharField(max_length=20, default='AAPL')
    interval2 = models.CharField(max_length=5, choices=INTERVAL_CHOICES, default='5mins')
    symbol3 = models.CharField(max_length=20, default='AAPL')
    interval3 = models.CharField(max_length=5, choices=INTERVAL_CHOICES, default='1min')
    keywords = models.TextField(max_length=256, default='AAPL;stock')

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class SettingsForm(ModelForm):
    class Meta:
        model = Settings
        fields = ['symbol1','interval1','symbol2','interval2','symbol3','interval3','keywords']