from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import FoodAndDrinks, PlayerInventory, ShopInventory

engine = create_engine('sqlite:///sandridge.db')
Session = sessionmaker(bind=engine)
session = Session()

def delete_records():
    session.query(food_or_drinks).delete()
    session.query(shop_inventory).delete()
    session.query(player_inventory).delete()
    session.commit()

def food_or_drinks():
    #seed data for FoodAndDrinks Table
    food_or_drink1 = FoodAndDrinks(name='Candy Bar', description='A sweet chocolate bar that provides a small boost of energy', price=1)
    food_or_drink2 = FoodAndDrinks(name='Beef Jerky', description='Dried and seasoned strips of beef, offering a good source of protein for quick', price=2.5)
    food_or_drink3 = FoodAndDrinks(name='Energy Drink', description='A popular caffeinated beverage that provides an instant energy boost', price=4)
    food_or_drink4 = FoodAndDrinks(name='Bag of Chips', description='A crispy bag of potato chips, perfect for snacking on the go', price=1.5)
    food_or_drink5 = FoodAndDrinks(name='Cheeseburger', description='A classic cheeseburger with a juicy beef patty, cheese and condiments', price=5)
    food_or_drink6 = FoodAndDrinks(name='Pancake', description='A stack of fluffy pancakes served with maple syrup and butter', price=4.5)
    food_or_drink7 = FoodAndDrinks(name='Milkshake', description='A thick and creamy milkshake', price=3.5)
    food_or_drink8 = FoodAndDrinks(name='French Fries', description='Crispy golden fries', price=2)
    food_or_drink9 = FoodAndDrinks(name='Bottled Water', description='A refreshing bottle of purified water', price=1.5)
    food_or_drink10 = FoodAndDrinks(name='Fruit Salad Cup', description='A cup filled with a mix of fresh fruits', price=3)
    food_or_drink11 = FoodAndDrinks(name='Granola Bar', description='A healthy snack bar made with oats, nuts, and dried fruits', price=2.5)
    food_or_drink12 = FoodAndDrinks(name='Protein Shake', description='A ready-to-drink protein shake to help with muscle recovery', price=4)

    session.add_all([food_or_drink1, food_or_drink2, food_or_drink3, food_or_drink4, food_or_drink5, food_or_drink6, food_or_drink7, food_or_drink8, food_or_drink9, food_or_drink10, food_or_drink11, food_or_drink12])

    session.commit()

def shop_inventory():
    pass

def player_inventory():
    pass

if __name__ == '__main__':
    delete_records()
    food_or_drinks()
