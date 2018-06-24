import requests
import time
import sqlite3
from recommender.model_classes import Restaurant as Rest


class PlacesDataProvider:
    """Places data provider interface"""

    def get_places(self, api_key, location, radius):
        """Returns places data"""
        raise NotImplementedError()


class GooglePlacesDataProvider(PlacesDataProvider):
    __URL = "https://maps.googleapis.com/maps/api/place/"

    def get_places(self, api_key, location, radius):
        places = []
        next_page_token = ""

        while True:
            time.sleep(2)
            if next_page_token is None:
                response = requests.get(self.__URL + "nearbysearch/json?" +
                                        "&location=" + location +
                                        "&radius=" + radius +
                                        "&key=" + api_key)
            else:
                response = requests.get(self.__URL + "nearbysearch/json?" +
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
