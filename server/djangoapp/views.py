from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method=="GET":
        return render(request,'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method=="GET":
        return render(request,'djangoapp/contact.html', context)


# Create a `login_request` view to handle sign in request
def login_request(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('./')
        else:
            messages.warning(request, f"Login failed ! ")
            return redirect('./')




# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('./')

# Create a `registration_request` view to handle sign up request
def registration_request(request):

    if request.method=="GET":
        return render(request, 'djangoapp/registration.html', {})

    elif request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')

        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
            messages.warning(request, f"Username {username} is already exists! ")

        except:
            logger.debug("{} is new user".format(username))

        if not user_exist:
            user = User.objects.create_user(username=username, password=password, first_name=firstname, last_name=lastname)
            login(request, user)
            messages.warning(request, f"Welcome {username}! ")
            return redirect('./')

    return render(request, 'djangoapp/registration.html',{})


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

