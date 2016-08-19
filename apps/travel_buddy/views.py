from django.shortcuts import render, redirect
from django.contrib import messages
from models import User, Trip, Booking
# Create your views here.
def index(request):
	return render(request, 'travel_buddy/index.html')

def travels(request):
	query = Booking.objects.all()
	context = {
		'bookings':query
	}
	return render(request, 'travel_buddy/dashboard.html', context)

def addpage(request):
	return render(request, 'travel_buddy/addpage.html')

def register(request):
	if request.method == 'POST':
		result = User.userManager.validateRegistration(request)
	#result is a tuple
	#It will hold a boolean, and the user we just created
		if result[0] == False:
			print 'No user created'
	 		#result[1] is the errorList
	 		print_messages(request, result[1])
	 		return redirect('/main')

	 	print 'User successfully created'	
		user = result[1]
		request.session['user'] = {
	 		'id': user.id,
	 		'name': user.name,
	 		'username': user.username
		 }

	return redirect('/travels')

def login(request):
	if request.method == 'POST':
		result = User.userManager.validateLogin(request)
	#result is a tuple
	#it will hold a boolean, and the user we just fetched if he exists
	if result[0] == False:
		print "No user Found"
		print_messages(request, result[1])
		return redirect('/main')

	print "User found. Successful login"
	user = result[1]
	request.session['user'] = {
		'id': user.id,
		'name': user.name,
		'username': user.username,
	}

	return redirect('/travels')

def print_messages(request, message_list):
	for message in message_list:
		messages.add_message(request, messages.INFO, message)

def logout(request):
	print 'Successful logout'
	request.session.clear()
	return redirect('/main')

def addTrip(request):
	#here we will add trip to Trips table 
	#AND then 'bond' the trip with the user aka
	#add them both to the Bookings table
	if request.method == 'POST':
		result = Trip.tripManager.validateCreation(request)
		if result[0] == False:
			print 'No trip created'
	 		#result[1] is the errorList
	 		print_messages(request, result[1])
	 		return redirect('/main')

	 	print 'Trip successfully created'	
		trip = result[1]
		request.session['trip'] = {
	 		'id': trip.id,
	 		'destination': trip.destination,
	 		'start_date': trip.start_date,
	 		'end_date': trip.end_date,
	 		'description': trip.description
		 }
		#here we will create the booking
		user = User.objects.get(id=int(request.POST['user_id']))

		Booking.objects.create(user=user, trip=trip)
		booking = Booking.objects.all()
		print "Booking created"
		print booking
		return redirect('/travels')

		return redirect('/travels')

def destination(request, id):

	booking = Booking.objects.get(trip=id)

	trip = Trip.objects.get(id=id)
	print id
	print trip
	context = {
		'trip':trip,
		'booking':booking
	}
	print context
	return render(request, 'travel_buddy/destination.html', context)






