import os
from dotenv import load_dotenv
import requests

load_dotenv()

backend_url = "http://localhost:3031"
print("BACKEND_URL =", backend_url)

sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/"
)


def get_request(endpoint, **kwargs):
    """Send GET request to Node backend."""
    params = ""

    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"

    if params:
        request_url = f"{backend_url}{endpoint}?{params}"
    else:
        request_url = f"{backend_url}{endpoint}"

    print(f"GET from {request_url}")

    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as e:
        print("Network exception occurred:", e)
        return []


def analyze_review_sentiments(text):
    """Send text to sentiment analyzer service."""
    request_url = f"{sentiment_analyzer_url}analyze/{text}"

    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected error: {err}, {type(err)}")
        print("Network exception occurred")
        return None


def post_review(data_dict):
    """Send review data to Node backend."""
    request_url = f"{backend_url}/insert_review"

    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
    except Exception as e:
        print("Network exception occurred:", e)
        return None
