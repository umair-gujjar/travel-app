from recommender.model_classes import Restaurant as Rest
from recommender.model_classes import Rating as Rat


class User:
    def __init__(self, id, name, relationshipdistance):
        self.id = id
        self.name = name
        self.relationshipdistance = relationshipdistance

    def rate(self, restaurant, value):
        restaurant.listOfRatings.append(Rat.Rating(self, value))










