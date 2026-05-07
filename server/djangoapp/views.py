from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout as django_logout
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import logging
import json

from .populate import initiate
from .models import CarMake, CarModel
from .restapis import (
    get_request,
    analyze_review_sentiments,
    post_review,
)
from . import restapis

print("RESTAPIS FILE LOADED FROM:", restapis.__file__)

logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    """Handle user login."""
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']

    user = authenticate(username=username, password=password)
    response_data = {"userName": username}

    if user is not None:
        login(request, user)
        response_data = {"userName": username, "status": "Authenticated"}

    return JsonResponse(response_data)


def logout(request):
    """Terminate user session."""
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration(request):
    """Handle user registration."""
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']

    username_exist = False

    try:
        User.objects.get(username=username)
        username_exist = True
    except User.DoesNotExist:
        logger.debug("%s is a new user", username)

    if not username_exist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email,
        )
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})

    return JsonResponse({"userName": username, "error": "Already Registered"})


def get_cars(request):
    """Return list of car models."""
    count = CarMake.objects.count()
    print(count)

    if count == 0:
        initiate()

    car_models = CarModel.objects.select_related('car_make')
    cars = [
        {"CarModel": cm.name, "CarMake": cm.car_make.name}
        for cm in car_models
    ]

    return JsonResponse({"CarModels": cars})


def get_dealerships(request, state="All"):
    """Return dealerships, optionally filtered by state."""
    print("RESTAPIS FILE LOADED FROM:", restapis.__file__)

    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)

    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_reviews(request, dealer_id):
    """Return reviews for a specific dealer."""
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)

        for review_detail in reviews:
            sentiment_response = analyze_review_sentiments(
                review_detail['review']
            )
            print(sentiment_response)

            if sentiment_response and 'sentiment' in sentiment_response:
                review_detail['sentiment'] = sentiment_response['sentiment']
            else:
                review_detail['sentiment'] = "neutral"

        return JsonResponse({"status": 200, "reviews": reviews})

    return JsonResponse({"status": 400, "message": "Bad Request"})


def get_dealer_details(request, dealer_id):
    """Return details for a specific dealer."""
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)

        if dealership and isinstance(dealership, list):
            dealership = dealership[0]

        return JsonResponse({"status": 200, "dealer": dealership})

    return JsonResponse({"status": 400, "message": "Bad Request"})


def add_review(request):
    """Add a review by forwarding it to the Node backend."""
    if request.user.is_anonymous:
        return JsonResponse({"status": 403, "message": "Unauthorized"})

    try:
        data = json.loads(request.body.decode('utf-8'))
        post_review(data)
        return JsonResponse({"status": 200})

    except Exception as e:
        print("ERROR IN add_review:", e)
        return JsonResponse(
            {"status": 401, "message": "Error in posting review"}
        )
