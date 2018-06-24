from recommender.model_classes import Rating
import sqlite3
class Restaurant:
    def __init__(self, id, name, lat, lng, google_ratings, types):
        self.id = id
        self.lat = lat
        self.lng = lng
        self.name = name
        self.listOfRatings = []
        self.google_rating = google_ratings
        self.types = types


