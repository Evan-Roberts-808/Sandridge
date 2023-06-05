from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FoodAndDrinks(Base):
    __tablename__ = 'food_and_drinks'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)

class PlayerInventory(Base):
    __tablename__ = 'player_inventory'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('food_and_drinks.id'))
    quantity = Column(Integer) 
    item = relationship('FoodAndDrinks') 


class ShopInventory(Base):
    pass

Base.metadata.create_all()