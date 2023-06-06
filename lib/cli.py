import click 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import FoodAndDrinks, PlayerInventory, ShopInventory 
from pyfiglet import Figlet
from PyInquirer import prompt, Separator

#python configure the database connection
engine = create_engine('sqlite:///sandridge.db')
Session = sessionmaker(bind=engine)
session = Session()


@click.group()
def cli():
    """Welcome to the Sandridge Shop!"""
    pass

@cli.command()
def shop():
    """Enter the shop."""
#fetch items from the shop_inventory table
    shop_items = session.query(ShopInventory).join(FoodAndDrinks).all()
#creating a query that will target the shopinventory table and join it with all of the data within the foodanddrinks table

#convert shop items to a list of dictionaries for PyInquirer
    choices = [
        {
            "name" : f"{item.item.name} - Price: {item.price}",
            "value" : item 
        }
        for item in shop_items
    ]

#add a separator and quit option 
    choices.append(Separator())
    choices.append({"name": "Quit", "value": None})

