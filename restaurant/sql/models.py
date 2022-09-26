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

class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    email = Column(String(50), nullable=False)
    
    @property
    def serialize(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email
        }
        
class Menu(Base):
    __tablename__ = 'menu'
    menu_id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(50))
    restaurant_id = Column(Integer,ForeignKey('restaurant.restaurant_id'))
    restaurant = relationship(Restaurant)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    user = relationship(User)
    
    @property
    def serialize(self):
        return {
            'menu_id': self.menu_id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'restaurant_id': self.restaurant_id,
            'user_id': self.user_id
        }