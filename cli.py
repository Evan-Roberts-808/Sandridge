from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.db.models import FoodAndDrinks, PlayerInventory, ShopInventory
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

engine = create_engine('sqlite:///lib/sandridge.db')
Session = sessionmaker(bind=engine)
session = Session()

console = Console()


class CLI:
    def __init__(self):
        self.console = Console()
        self.choices = {
            "1": self.show_shop,
            "2": self.show_inventory,
            "3": self.buy_item,
            "q": self.quit
        }

    def restock_shop(self):
        food_and_drinks = session.query(FoodAndDrinks).all()
        for item in food_and_drinks:
            existing_item = session.query(ShopInventory).filter_by(item_id=item.id).first()
            if not existing_item:
                shop_item = ShopInventory(
                    item_id=item.id, price=item.price, quantity=10)
                session.add(shop_item)
        session.commit()

    def show_shop(self):
        table = Table(title="Shop Inventory",
                      show_header=True, header_style="bold")
        table.add_column("ID", justify="right")
        table.add_column("Item")
        table.add_column("Price", justify="right")
        table.add_column("Quantity", justify="right")

        shop_items = session.query(ShopInventory).join(FoodAndDrinks).all()

        if not shop_items:
            self.console.print(
                "The shop is currently out of stock. Please check back later.")
            return

        for item in shop_items:
            table.add_row(str(item.item_id), item.item.name, str(item.price), str(item.quantity))

        self.console.print(table)

    def buy_item(self):
        shop_items = session.query(ShopInventory).join(FoodAndDrinks).all()

        if not shop_items:
            self.console.print(
                "The shop is currently out of stock. Please check back later.")
            return

        item_choices = {}
        for item in shop_items:
            item_choices[str(item.item_id)] = item

        item_prompt = Prompt.ask(
            "Enter the ID of the item you want to purchase:", choices=item_choices)

        if not item_prompt:
            self.console.print(
                "Thank you for visiting the Sandridge shop! See you next time!")
            return

        selected_item = item_choices[item_prompt]
        quantity = int(Prompt.ask("Enter the quantity you want to purchase:"))

        if quantity <= selected_item.quantity:
            selected_item.quantity -= quantity
            player_item = PlayerInventory(
                item_id=selected_item.item_id, quantity=quantity)
            session.add(player_item)
            session.commit()
            self.console.print(
                f"You have purchased {quantity} {selected_item.item.name}.")
        else:
            self.console.print("Sorry, the selected item is out of stock.")

    def show_inventory(self):
        table = Table(title="Player Inventory",
                      show_header=True, header_style="bold")
        table.add_column("ID", justify="right")
        table.add_column("Item")
        table.add_column("Quantity", justify="right")

        inventory_items = session.query(
            PlayerInventory).join(FoodAndDrinks).all()

        if not inventory_items:
            self.console.print("Your inventory is empty.")
            return

        for item in inventory_items:
            table.add_row(str(item.item_id), item.item.name,
                          str(item.quantity))

        self.console.print(table)

    def quit(self):
        self.console.print(
            "Thank you for visiting the Sandridge shop! See you next time!")
        raise SystemExit

    def run(self):
        self.restock_shop()
        while True:
            self.console.print("[bold]Sandridge Shop[/bold]")
            self.console.print("1. Show Shop Inventory")
            self.console.print("2. Show Player Inventory")
            self.console.print("3. Buy Item")
            self.console.print("q. Quit")

            choice = Prompt.ask("What would you like to do?",
                                choices=["1", "2", "3", "q"])

            if choice in self.choices:
                self.choices[choice]()
            else:
                self.console.print("Invalid choice. Please try again.")


cli = CLI()
cli.run()
