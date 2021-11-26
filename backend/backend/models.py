from django.db import models

class Task(models.Model):
	Issue = models.CharField(max_length=200)
	Due = models.DateTimeField()
	Tag = models.CharField()
	CompleteStatus = models.BooleanField(default=False)

class User(models.Model):
	UserName = models.CharField(max_length=30)
	UserPassword = models.CharField(max_length=30)
	Stock = models.CharField(max_length=30)
	News = models.CharField(max_length=30)


