from django.db import models
from django.db.models import CharField


class User(models.Model):
	Name = models.CharField(max_length=30)
	Stock = models.CharField(max_length=30)
	News = models.CharField(max_length=30)

class Task(models.Model):
	Issue = models.CharField(max_length=200)
	Due = models.DateTimeField()
	Tag = models.CharField()

	def __str__(self):
		return self.title