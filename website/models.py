from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.db import models

def upload_location(instance, filename):
	return ("%s/%s" %(instance.id, filename))

# Create your models here.
class Workshop(models.Model):
	title = models.CharField(max_length = 200)
	about = models.TextField(max_length = 700 )
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	duration = models.CharField(max_length = 100)
	tag = models.CharField(max_length = 100, null = True)
	schedule = models.FileField(upload_to=  upload_location)
	instruct_part = models.TextField(max_length = 1000)
	instruct_coord = models.TextField(max_length = 1000)

	def get_absolute_url(self):
		return reverse("website:details", kwargs= {"workshop_id": self.id})

class Profile(models.Model):
    user = models.ForeignKey(User)
    interests = models.ForeignKey(Workshop)
    email = models.CharField(max_length=128)

class Slot(models.Model): # Slot
	user = models.ForeignKey(User)
	workshop = models.ForeignKey(Workshop)
	dates = models.CharField(max_length = 200)
	status = models.CharField(max_length = 100)

class Booking(models.Model):
	user = models.ForeignKey(User)  # Booking
	slot = models.ForeignKey(Slot)
	address = models.CharField(max_length = 200)
	participants = models.CharField(max_length = 50)

	def get_absolute_url(self):
		return reverse("website:slots", kwargs= {"workshop_id": self.id})
