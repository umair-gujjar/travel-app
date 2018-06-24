from sqlalchemy import Column, Integer, Float, String
from database.database import Base

class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    lat = Column(Float)
    long = Column(Float)

    def __init__(self, name=None, lat=None, long=None):
        self.name = name
        self.lat = lat
        self.long = long

    def __repr__(self):
        return '<Restaurant %r>' % (self.name)