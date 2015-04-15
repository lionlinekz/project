from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Employee(models.Model):
	user = models.OneToOneField(User)
	is_admin = models.BooleanField(default=False)
	position = models.CharField(max_length=128, default="")
	picture = models.ImageField(upload_to='profile_images', blank=True)

	def __unicode__(self):
		return self.user.username

class Task(models.Model):
	owner = models.ForeignKey(Employee)
	date_published = models.DateField()
	date_due = models.DateField()
	state = models.BooleanField()
	title = models.CharField(max_length=256)
	description = models.CharField(max_length=1024)

	def __unicode__(self):
		return self.title

class Report(models.Model):
	task = models.ForeignKey(Task)
	title = models.CharField(max_length=256)
	description = models.CharField(max_length=1024)
	owner = models.ForeignKey(Employee)
	date_published = models.DateField()
	is_seen = models.BooleanField(default=False)

	def __unicode__(self):
		return self.description

class Message(models.Model):
	owner = models.ForeignKey(Employee)
	text = models.CharField(max_length=1024)
	date_published = models.DateField()
	task = models.ForeignKey(Task)
	is_seen = models.BooleanField(default=False)

	def __unicode__(self):
		return self.text