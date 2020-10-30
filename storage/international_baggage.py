from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class InternationalBaggage(Base):
    """ International Baggage input """
    
    __tablename__ = "international_baggage"
    
    id = Column(Integer, primary_key=True)
    baggage_id = Column(String(100), nullable=False)
    weight_kg = Column(Integer, nullable=False)
    destination = Column(String(250), nullable=False)
    timestamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)
    
    def __init__(self, baggage_id, weight_kg, destination, timestamp):
        """ Initialize International Baggage Information """
    
        self.baggage_id = baggage_id
        self.weight_kg = weight_kg
        self.destination = destination
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now()
        
    def to_dict(self):
        """ converts baggage info to dictionary representation """
        
        dict = {}
        dict['id'] = self.id
        dict['baggage_id'] = self.baggage_id
        dict['weight_kg'] = self.weight_kg
        dict['destination'] = self.destination
        dict['timestamp'] = self.timestamp
        dict['date_created'] = self.date_created
        
        return dict
    