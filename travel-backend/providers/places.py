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
                                        "&key=" + api_key)
            response_json = response.json()
            places.extend(response_json['results'])

            if 'next_page_token' in response_json:
                next_page_token = response_json['next_page_token']
            else:
                break


        return places

Caller = GooglePlacesDataProvider()
places = Caller.get_places("AIzaSyDS40mCvePWcb9_eI_SErFQpt98UoTI3UI", "50.04, 14.4", "100")

conn = sqlite3.connect('restaurant.db')

c = conn.cursor()




#for i in range(-2, 2):
 #   for j in range(-2, 2):

 #       places = Caller.get_places("AIzaSyDS40mCvePWcb9_eI_SErFQpt98UoTI3UI", "50., 14.4", "1000")






#c.execute("DELETE FROM users")
#for i in range(0, 50):
#    x = U.User(i+1, 'Name' + str(i + 1), randint(1, 5))
#    c.execute("INSERT INTO users VALUES (:id, :name, :distance)", {'id': x.id, 'name': x.name, 'distance': x.relationshipdistance})

c.execute("CREATE ")
conn.commit()

conn.close()

c.execute("SELECT * FROM users")
print(c.fetchall())

conn.commit()

conn.close()
