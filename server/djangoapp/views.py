# Uncomment the required imports before adding the code

# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
# from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


# ✅ New view to get cars (CarMake and CarModel info)
def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        })
    return JsonResponse({"CarModels": cars})


# ✅ View to render list of dealerships
def get_dealerships(request, state="All"):
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


# ✅ View to get details of a single dealer
def get_dealer_details(request, dealer_id):
    if(dealer_id):
        endpoint = "/fetchDealer/" + str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": [dealership]})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


# ✅ View to get reviews for a specific dealer, including sentiment
'''
def get_dealer_reviews(request, dealer_id):
    if(dealer_id):
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            print(response)
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})
'''
'''
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)
        print("Raw reviews fetched:", reviews)

        try:
            for review_detail in reviews:
                sentiment = analyze_review_sentiments(review_detail['review'])
                review_detail['sentiment'] = sentiment['sentiment']
        except Exception as e:
            print("🔥 Error analyzing sentiment:", e)
            return JsonResponse({"status": 500, "message": "Sentiment analysis failed"})

        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})
'''
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)
        print("Raw reviews fetched:", reviews)

        for review_detail in reviews:
            try:
                sentiment = analyze_review_sentiments(review_detail['review'])
                if sentiment and 'sentiment' in sentiment:
                    review_detail['sentiment'] = sentiment['sentiment']
                else:
                    review_detail['sentiment'] = "neutral"  # fallback
            except Exception as e:
                print("🔥 Sentiment error:", e)
                review_detail['sentiment'] = "neutral"  # fallback

        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# ✅ View to submit a review (POST only if authenticated)
@csrf_exempt
def add_review(request):
    if request.user.is_anonymous == False:
        data = json.loads(request.body)
        try:
            response = post_review(data)
            print(response)
            return JsonResponse({"status": 200})
        except:
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})

@csrf_exempt
def register_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return JsonResponse({"status": "error", "message": "Missing fields"}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({"status": "error", "message": "User already exists"}, status=400)
        user = User.objects.create_user(username=username, password=password)
        return JsonResponse({"status": "success", "message": "User created"})