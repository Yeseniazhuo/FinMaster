from django.db import models


class User(models.Model):
	Name = models.CharField(max_length=30)
	Stock = models.CharField(max_length=30)
	News = models.CharField(max_length=30)

class Task(models.Model):
	Issue = models.CharField(max_length=200)
	Due = models.DateTimeField()
	Tag = models.CharField()