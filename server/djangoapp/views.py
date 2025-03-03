from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel, CarMake
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_by_id_from_cf, post_request
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
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact_us.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/registration.html', context)
    else:
        return render(request, 'djangoapp/user_login_bootstrap.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://517fe93c.us-south.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context["dealerships"] = dealerships
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    url = "https://517fe93c.us-south.apigw.appdomain.cloud/api/review/"
    # Get dealers from the URL
    reviews = get_dealer_reviews_from_cf(url, dealer_id)
    context['reviews'] = reviews
    context['dealer'] = dealer_id
    # Concat all dealer's short name
    # dealer_details = ' '.join([dealer.review for dealer in reviews])
    return render(request, 'djangoapp/dealer_details.html', context)

def get_dealer_name(dealer_id):
        url = "https://517fe93c.us-south.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealer_name = get_dealer_by_id_from_cf(url, dealer_id).full_name
        return dealer_name


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
def add_review(request, dealer_id):
    if request.method == "GET":
        context = {}
        cars = list(CarModel.objects.filter(dealer_id=dealer_id))
        context["dealer_name"] = get_dealer_name(dealer_id)
        context["cars"] = cars
        context["dealer_id"] = dealer_id
        return render(request, 'djangoapp/add_review.html', context)
    if request.method == "POST":
        url = "https://517fe93c.us-south.apigw.appdomain.cloud/api/review"
        if request.user.is_authenticated:
            car = CarModel.objects.get(id=request.POST["car"])
            review = {}
            review["time"] = datetime.utcnow().isoformat()
            review["name"] = request.user.get_username()
            review["dealership"] = dealer_id
            review["review"] = request.POST["content"]
            review["car_model"] = car.name
            review["car_year"] = car.year.strftime("%Y") 
            review["car_make"] = car.manufacturer.name
            review["purchase_date"] = request.POST["purchase_date"]
            if request.POST["purchase"] == 'on':
                review["purchase"] = True
            review["purchase"] = False
            json_payload = {}
            json_payload = review
            print(json_payload)
            post_request(url, json_payload, dealerId=dealer_id)

            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
