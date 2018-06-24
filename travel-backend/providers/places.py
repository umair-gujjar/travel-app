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

Caller = GooglePlacesDataProvider()
restaurant_list = []




conn = sqlite3.connect('restaurant.db')

c = conn.cursor()

for i in range(-2, 2):
    for j in range(-2, 2):
        places = Caller.get_places("AIzaSyDS40mCvePWcb9_eI_SErFQpt98UoTI3UI",
                                   str(50.084062 + i / 100) + ', ' + str(14.421809 + j / 100),
                                   "500")
        for k in range(0, 59):
            ident = places[k]['id']
            x = places[k]['geometry']['location']['lat']
            y = places[k]['geometry']['location']['lat']
            name = places[k]['name']
            restaurant_list.append(Rest.Restaurant(ident, name, x, y))

restaurant_dictionary = dict()
for restaurant in restaurant_list:
    if not restaurant_dictionary.__contains__(restaurant.id):
        restaurant_dictionary[restaurant.id] = restaurant

for key in restaurant_dictionary.keys():
    print(restaurant_dictionary[key].name)

print(len(restaurant_dictionary))



#c.execute("""
 #   CREATE TABLE restaurants (
  #      id string,
   #     name string,
    #    lat string,
     #   lng string
      #  )""")
for key in restaurant_dictionary.keys():
    A = restaurant_dictionary[key]
    c.execute("""
        INSERT INTO restaurants VALUES (:id, :name, :lat, :lng)
            """, {'id': A.id, 'name': A.name, 'lat': A.lat, 'lng': A.lon})

conn.commit()

conn.close()
