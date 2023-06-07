from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///sandridge.db')
Session = sessionmaker(bind=engine)
session = Session()

class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(String())
    description = Column(String())
    shop_inventory = relationship('ShopInventory', back_populates='location')


class FoodAndDrinks(Base):
    __tablename__ = 'food_and_drinks'
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    description = Column(String())
    price = Column(Integer())
    shop_inventory = relationship('ShopInventory', back_populates='item')


class PlayerInventory(Base):
    __tablename__ = 'player_inventory'
    id = Column(Integer(), primary_key=True)
    item_id = Column(Integer(), ForeignKey('food_and_drinks.id'))
    quantity = Column(Integer())
    item = relationship('FoodAndDrinks')


class ShopInventory(Base):
    __tablename__ = 'shop_inventory'
    id = Column(Integer(), primary_key=True)
    item_id = Column(Integer(), ForeignKey('food_and_drinks.id'))
    price = Column(Integer())
    quantity = Column(Integer())
    item = relationship('FoodAndDrinks', back_populates='shop_inventory')
    location_id = Column(Integer(), ForeignKey('locations.id'))
    location = relationship('Location', back_populates='shop_inventory')

Base.metadata.create_all(bind=engine)
