from sqlalchemy import Column, Integer, Float, String


class Restaurant:
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(50))
    lat = Column(Float)
    lng = Column(Float)
    google_ratings = Column(Integer)
    types = Column(String(200))

    def __init__(self, id=None, name=None, lat=None, lng=None, google_ratings=None, types=None):
        self.id = id
        self.name = name
        self.lat = lat
        self.lng = lng
        self.google_ratings = google_ratings
        self.types = types

    def __repr__(self):
        return '<Restaurant %r>' % (self.name)