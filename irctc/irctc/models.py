from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from time import time
from datetime import date
from datetime import datetime
from django.utils.encoding import python_2_unicode_compatible
	
class UserDetail(models.Model):
	user = models.ForeignKey(User)
	address = models.TextField
	mobileNo = models.IntegerField(null=False)

class Reservation(models.Model):
	userDetail = models.ForeignKey('UserDetail')
	firstName = models.CharField(max_length=30)	
	lastName = models.CharField(max_length=50)	
	gender = models.CharField(max_length=10)
	age = models.IntegerField()
	address = models.TextField()
	mobileNo = models.IntegerField(null=False)
	pnrNo = models.TextField()
	journeyDate = models.DateTimeField()
	className = models.CharField(max_length=50)
	seatNo = models.IntegerField()
	source = models.ForeignKey('Location',related_name='source')
	destination = models.ForeignKey('Location',related_name='destination')
	train = models.ForeignKey('Train')
	def __unicode__(self):
		return self.firstName

class Location(models.Model):
	lat = models.FloatField()
	lng = models.FloatField()
	locationText = models.CharField(max_length=50)

class Train(models.Model):
	trainNo = models.IntegerField()
	trainName = models.CharField(max_length=100)
	trainSource = models.ForeignKey('Location',related_name='trainSource')
	trainDestination = models.ForeignKey('Location',related_name='trainDestination')
	arrivalTime = models.TimeField(null=True)
	departureTime = models.TimeField(null=True)
	date = models.DateField()
	def __unicode__(self):
		return self.trainName

class Station(models.Model):
	stationName = models.CharField(max_length=100)
	arrivalTime = models.TimeField(null=True)
	departureTime = models.TimeField(null=True)
	train = models.ForeignKey('Train')

	def __unicode__(self):
		return self.stationName

