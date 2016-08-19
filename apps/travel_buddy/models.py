from __future__ import unicode_literals

from django.db import models
import bcrypt

# Create your models here.
class UserManager(models.Manager):
	def validateRegistration(self, request):
		errorList = []

		if len(request.POST['name']) < 3 or len(request.POST['username']) < 3:
			errorList.append('Please enter a valid Name and Username (at least 3 characters)')

		if str.isalpha(str(request.POST['name'])) == False:
			errorList.append('Please enter a valid Name (letters only)')

		if len(request.POST['password']) < 8 or request.POST['password'] != request.POST['c_password']:
			errorList.append('Passwords must match and be at least 8 characters')

		if len(errorList) > 0:
			return (False, errorList)
		#if it makes it here, there are no errors
		#time to hash the pw and create the user

		pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

		user = self.create(name=request.POST['name'], username=request.POST['username'], pw_hash=pw_hash)

		return (True, user)

	def validateLogin(self, request):
		user = self.filter(username=request.POST['username'])

		if len(user) == 0:
			return (False, ['Incorrect Username/password'])

		password = request.POST['password'].encode()
		if bcrypt.hashpw(password, user[0].pw_hash.encode()):
			return (True, user[0])
class TripManager(models.Manager):
	def validateCreation(self, request):
		errorList = []

		if len(request.POST['destination']) < 1 or len(request.POST['description']) < 1 or len(request.POST['start_date']) < 1 or len(request.POST['end_date']) < 1:
			errorList.append('Fill out all fields')

		if len(errorList) > 0:
			return (False, errorList)

		#if it makes it here there are no errors
		#time to create the trip

		trip = self.create(destination=request.POST['destination'], start_date=request.POST['start_date'], end_date=request.POST['end_date'], description=request.POST['description'])

		return (True, trip)

class User(models.Model):
	name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	pw_hash = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	userManager = UserManager()
	objects = models.Manager()

class Trip(models.Model):
	destination = models.CharField(max_length=255)
	start_date = models.DateField()
	end_date = models.DateField()
	description = models.TextField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	tripManager = TripManager()
	objects = models.Manager()

class Booking(models.Model):
	user = models.ForeignKey(User, related_name="user")
	trip = models.ForeignKey(Trip, related_name="trip")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)



