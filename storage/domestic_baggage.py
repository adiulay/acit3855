from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime

class DomesticBaggage(Base):
    """ Domestic Baggage input """
    
    __tablename__ = "domestic_baggage"
    
    id = Column(Integer, primary_key=True)
    baggage_id = Column(String(100), nullable=False)
    weight_kg = Column(Integer, nullable=False)
    destination_province = Column(String(250), nullable=False)
    postal_code = Column(String(7), nullable=False)
    timestamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)
    
    
    def __init__(self, baggage_id, weight_kg, destination_province, postal_code, timestamp):
        """ Initializes domestic baggage information """
        
        self.baggage_id = baggage_id
        self.weight_kg = weight_kg
        self.destination_province = destination_province
        self.postal_code = postal_code
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now() # Sets the date/time when recorded
        
    def to_dict(self):
        """ converts baggage info to dictionary representation """
        
        dict = {}
        dict['id'] = self.id
        dict['baggage_id'] = self.baggage_id
        dict['weight_kg'] = self.weight_kg
        dict['destination_province'] = self.destination_province
        dict['postal-code'] = self.postal_code
        dict['timestamp'] = self.timestamp
        dict['date_created'] = self.date_created
        
        return dict
        