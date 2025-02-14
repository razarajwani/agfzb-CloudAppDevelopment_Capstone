import requests
import json
import os
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["docs"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                   full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealer_id)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["docs"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = DealerReview(
                id="",
                name="",
                dealership=dealer_doc['dealership'],
                purchase=dealer_doc['purchase'] ,
                purchase_date=dealer_doc['purchase_date'] if dealer_doc['purchase'] else "",
                review=dealer_doc['review'],
                car_make=dealer_doc['car_make'] if dealer_doc['purchase'] else "None",
                car_model=dealer_doc['car_model'] if dealer_doc['purchase'] else "None",
                car_year=dealer_doc['car_year'] if dealer_doc['purchase'] else "-",
                sentiment=analyze_review_sentiments(dealer_doc['review'])
            )
            results.append(dealer_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def analyze_review_sentiments(review):
    params = dict()
    params["text"] = review
    params["version"] = "2018-09-21"
    params["features"] = dict(sentiment=dict())
    params["return_analyzed_text"] = True
    params["language"] = "en"

    url = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/2cb9732a-5a0d-4b3b-bdc4-4be63c05cad3/v1/analyze'

    response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                            auth=HTTPBasicAuth('apikey', os.getenv('NLU_API_KEY', 'h3j6DSSEJmoapOMtR1E0mj_Pi058-C9RNVYUHRdM-5Fv')))

    return json.loads(response.text)['sentiment']['document']['label']
