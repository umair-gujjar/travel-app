from recommender.model_classes import Rating

class Restaurant:
    def __init__(self, name, location, category):
        self.name = name
        self.location = location
        self.category = category
        self.listOfRatings = []


