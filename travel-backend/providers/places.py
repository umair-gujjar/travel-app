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



#
# restaurant_list = []
# caller = GooglePlacesDataProvider()
# rating = ''
# for i in range(-2, 2):
#     for j in range(-2, 2):
#         places = caller.get_places("AIzaSyDS40mCvePWcb9_eI_SErFQpt98UoTI3UI",
#                                    str(50.084062 + i / 100) + ', ' + str(14.421809 + j / 100),
#                                    "500")
#         for k in range(0, 59):
#             ident = places[k]['id']
#             x = places[k]['geometry']['location']['lat']
#             y = places[k]['geometry']['location']['lat']
#             name = places[k]['name']
#             if places[k].__contains__('rating'):
#                 rating = places[k]['rating']
#             types = ','.join(places[k]['types'])
#             restaurant_list.append(Rest.Restaurant(ident, name, x, y, rating, types))
#
# restaurant_dictionary = dict()
# for restaurant in restaurant_list:
#     if not restaurant_dictionary.__contains__(restaurant.id):
#         restaurant_dictionary[restaurant.id] = restaurant
#
# for key in restaurant_dictionary.keys():
#     print(restaurant_dictionary[key].name)
#
# print(len(restaurant_dictionary))
#
# for key in restaurant_dictionary.keys():
#     A = restaurant_dictionary[key]
#     c.execute("""
#         INSERT INTO restaurants VALUES (:id, :lat, :lng, :name, :google_ratings, :types)
#             """, {'id': A.id, 'lat': A.lat, 'lng': A.lng, 'name': A.name, 'google_ratings': A.google_rating, 'types': A.types})
conn = sqlite3.connect('restaurant.db')
c = conn.cursor()

conn.commit()
conn.close()