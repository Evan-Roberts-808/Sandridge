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

    #questions
    questions = [
        {
            "type": "list", 
            "name": "item",
            "message": "select an item to purchase: ",
            "choices": choices
        },   
        {
            "type": "input",
            "name": "quantity",
            "message": "how many would you like? ",
            "when": lambda answers: answers["item"] is not None 
        }
    ]
    answers = prompt(questions)
    
    if answers["item"] is None:
        click.echo("Thank you for visiting the Sandridge shop! See you next time!")
        return
    selected_item = answers["item"]
    quantity = int(answers["quantity"])
    
    #checks if selected item is already in the shop inventory
    if quantity <= selected_item.quantity:
        #creates a new player inventory record
        player_item = PlayerInventory(item_id=selected_item.item_id, quantity = quantity)
        session.add(player_item)
        session.commit()
        click.echo(f'You have purchased {quantity} {selected_item.item.name}.')
        
if __name__ == '__main__':
    cli()