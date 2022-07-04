from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
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
            messages.success(request, f"Welcome {user.first_name} to BestCars! ")
            return redirect('djangoapp:index')
        else:
            messages.warning(request, f"Login failed! Please ensure the username and password are valid. ")
            return redirect('djangoapp:index')




# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

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
            messages.success(request, f"Welcome {user.first_name} to BestCars! ")
            return redirect('djangoapp:index')

    return render(request, 'djangoapp/registration.html',{})


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}

        url = "https://eb64b315.us-south.apigw.appdomain.cloud/api/dealership"
        context['dealerships'] = get_dealers_from_cf(url)

        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {}
        url = "https://eb64b315.us-south.apigw.appdomain.cloud/api/review"
        context['dealer_reviews'] = get_dealer_reviews_from_cf(url, dealer_id)
        context['dealer'] = dealer_id

        # Return a list of dealer short name
        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.method == "GET":
        context = {}
        context['dealer_id'] = dealer_id
        context['cars'] = CarModel.objects.filter(dealership=dealer_id)

        return render(request, 'djangoapp/add_review.html', context)
    if request.method == "POST" and request.user.is_authenticated:
        url = "https://eb64b315.us-south.apigw.appdomain.cloud/api/review"
        review_payload = dict()
        review_payload["time"] = datetime.utcnow().isoformat()
        review_payload["dealership"] = dealer_id
        review_payload["review"] = request.POST.get('review', "")
        review_payload["purchase"] = request.POST.get('purchase', False)

        if review_payload['purchase']:
            car = CarModel.objects.filter(id=int(request.POST.get('car')))[0]

            review_payload["purchase_date"] = request.POST.get('purchasedate')
            review_payload["car_model"] = car.name
            review_payload["car_year"] = car.year.strftime("%Y")
            review_payload["car_make"] = car.maker.name

        response = post_request(url, json_payload=dict(review=review_payload))

        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)