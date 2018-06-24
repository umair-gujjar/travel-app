import requests
import time
import sqlite3
# from ...recommender.model_classes import Restaurant as Rest


def get_places(api_key, location, radius):
    __URL = "https://maps.googleapis.com/maps/api/place/"
    places = []
    next_page_token = ""

    while True:
        time.sleep(2)
        if next_page_token is None:
            response = requests.get(__URL + "nearbysearch/json?" +
                                    "&location=" + location +
                                    "&radius=" + radius +
                                    "&key=" + api_key)
        else:
            response = requests.get(__URL + "nearbysearch/json?" +
                                    "&location=" + location +
                                    "&radius=" + radius +
                                    "&pagetoken=" + next_page_token +
                                    "&key=" + api_key +
                                    "&keyword = restaurant")
        response_json = response.json()
        places.extend(response_json['results'])

        if 'next_page_token' in response_json:
            next_page_token = response_json['next_page_token']
        else:
            break

    return places
