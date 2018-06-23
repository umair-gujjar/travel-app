import requests


class PlacesDataProvider:
    """Places data provider interface"""

    def get_places(self, location, radius):
        """Returns places data"""
        raise NotImplementedError()


class GooglePlacesDataProvider(PlacesDataProvider):
    __URL = "https://maps.googleapis.com/maps/api/place/"
    __API_KEY = "XXSECRETXX"

    def get_places(self, location, radius):
        response = requests.get(self.__URL + "nearbysearch/json?" +
                                "&location=" + location +
                                "&radius=" + radius + "&maxResults=19"
                                "&key=" + self.__API_KEY)
        return response.json()
