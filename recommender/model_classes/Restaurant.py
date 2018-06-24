from recommender.model_classes import Rating
import sqlite3
class Restaurant:
    def __init__(self, id, name, lat, lon):
        self.id = id
        self.lat = lat
        self.lon = lon
        self.name = name
        self.listOfRatings = []


