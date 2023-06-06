from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import FoodAndDrinks

engine = create_engine('sqlite:///sandridge.db')
Session = sessionmaker(bind=engine)
session = Session()


def delete_records():
    session.query(FoodAndDrinks).delete()
    session.commit()


def seed_food_or_drinks():
    # seed data for FoodAndDrinks Table
    food_and_drinks_data = [
        {
            'name': 'Candy Bar',
            'description': 'A sweet chocolate bar that provides a small boost of energy',
            'price': 1
        },
        {
            'name': 'Beef Jerky',
            'description': 'Dried and seasoned strips of beef, offering a good source of protein for quick',
            'price': 2.5
        },
        {
            'name': 'Energy Drink',
            'description': 'A popular caffeinated beverage that provides an instant energy boost',
            'price': 4
        },
        {
            'name': 'Bag of Chips',
            'description': 'A crispy bag of potato chips, perfect for snacking on the go',
            'price': 1.5
        },
        {
            'name': 'Cheeseburger',
            'description': 'A classic cheeseburger with a juicy beef patty, cheese and condiments',
            'price': 5
        },
        {
            'name': 'Pancake',
            'description': 'A stack of fluffy pancakes served with maple syrup and butter',
            'price': 4.5
        },
        {
            'name': 'Milkshake',
            'description': 'A thick and creamy milkshake',
            'price': 3.5
        },
        {
            'name': 'French Fries',
            'description': 'Crispy golden fries',
            'price': 2
        },
        {
            'name': 'Bottled Water',
            'description': 'A refreshing bottle of purified water',
            'price': 1.5
        },
        {
            'name': 'Fruit Salad Cup',
            'description': 'A cup filled with a mix of fresh fruits',
            'price': 3
        },
        {
            'name': 'Granola Bar',
            'description': 'A healthy snack bar made with oats, nuts, and dried fruits',
            'price': 2.5
        },
        {
            'name': 'Protein Shake',
            'description': 'A ready-to-drink protein shake to help with muscle recovery',
            'price': 4
        }
    ]

    for item_data in food_and_drinks_data:
        item = FoodAndDrinks(**item_data)
        session.add(item)

    session.commit()
    
if __name__ == '__main__':
    delete_records()
    seed_food_or_drinks()
    print("Data seeding complete")
