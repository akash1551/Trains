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

class Passenger(models.Model):
	firstName = models.CharField(max_length=30)	
	lastName = models.CharField(max_length=50)	
	gender = models.CharField(max_length=10)
	age = models.IntegerField()
	address = models.TextField()
	mobileNo = models.IntegerField(null=False)
	reservation = models.ManyToManyField('Reservation')

class Train(models.Model):
	trainNo = models.IntegerField()
	trainName = models.CharField(max_length=100)
	trainSource = models.CharField(max_length=100)
	trainDestination = models.CharField(max_length=100)
	arrivalTime = models.TimeField(null=True)
	departureTime = models.TimeField(null=True)

	def __unicode__(self):
		return self.trainName

class Reservation(models.Model):
	pnrNo = models.UUIDField()
	journeyDate = models.DateTimeField()
	className = models.CharField(max_length=50)
	seatNo = models.IntegerField()
	source = models.CharField(max_length=100)
	destination = models.CharField(max_length=100)
	train = models.ForeignKey('Train')

class Station(models.Model):
	stationName = models.CharField(max_length=100)
	arrivalTime = models.TimeField(null=True)
	departureTime = models.TimeField(null=True)
	train = models.ForeignKey('Train')

	def __unicode__(self):
		return self.stationName

class Location