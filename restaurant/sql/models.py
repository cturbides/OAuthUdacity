from restaurant.sql import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Float, Integer, ForeignKey, String

class Restaurant(Base):
    __tablename__ = 'restaurant'
    restaurant_id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, unique=True)
    
    @property
    def serialize(self):
        return {
            'restaurant_id':self.restaurant_id,
            'name': self.name
        }

class Menu(Base):
    __tablename__ = 'menu'
    menu_id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(50))
    restaurant_id = Column(Integer,ForeignKey('restaurant.restaurant_id'))
    restaurant = relationship(Restaurant)
    
    @property
    def serialize(self):
        return {
            'menu_id': self.menu_id,
            'name': self.name,
            'price': self.price,
            'description': self.description
        }