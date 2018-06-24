from sqlalchemy import Column, Integer, Float, String
from database.database import db_session, Base

class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    lat = Column(Float)
    lng = Column(Float)
    google_ratings = Column(Integer)
    types =  Column(String(200))

    def __init__(self, id=None, name=None, lat=None, lng=None, google_ratings=None, types=None):
        self.id = id
        self.name = name
        self.lat = lat
        self.lng = lng
        self.google_ratings
        self.types

    def __repr__(self):
        return '<Restaurant %r>' % (self.name)