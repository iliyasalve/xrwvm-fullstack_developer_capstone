import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")


def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"

    request_url = f"{backend_url}{endpoint}?{params.rstrip('&')}" 
    print("GET from {}".format(request_url))
    
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as e:
        print(f"Network exception occurred: {e}")


def analyze_review_sentiments(text):
    request_url = f"{sentiment_analyzer_url}analyze/{text}"  
    
    try:
        response = requests.get(request_url)
        response.raise_for_status()  
        json_response = response.json()
        
        if 'sentiment' in json_response:
            return json_response
        else:
            print("Sentiment not found in the response")
            return None  
    except requests.exceptions.RequestException as req_err:
        print(f"Request error: {req_err}")
        return None 
    except ValueError as json_err:
        print(f"JSON decoding error: {json_err}")
        return None  
    except Exception as err:
        print(f"Unexpected error: {err}")
        return None 


def post_review(data_dict):
    request_url = f"{backend_url}/insert_review" 
    
    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
    except Exception as e:
        print(f"Network exception occurred: {e}")

