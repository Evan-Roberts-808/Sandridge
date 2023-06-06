from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.db.models import FoodAndDrinks, PlayerInventory, ShopInventory
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text

engine = create_engine('sqlite:///sandridge.db')
Session = sessionmaker(bind=engine)
session = Session()

console = Console()

def show_shop():
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Item", style="cyan")
    table.add_column("Price", justify="right", style="green")

    shop_items = session.query(ShopInventory).join(FoodAndDrinks).all()

    if not shop_items:
        console.print("The shop is currently out of stock. Please check back later.")
        return

    for item in shop_items:
        table.add_row(item.item.name, str(item.price))

    console.print(table)


def buy_item():
    shop_items = session.query(ShopInventory).join(FoodAndDrinks).all()

    if not shop_items:
        console.print("The shop is currently out of stock. Please check back later.")
        return

    item_choices = {}
    for index, item in enumerate(shop_items, start=1):
        item_choices[str(index)] = item

    item_prompt = Prompt.ask("Select an item to purchase:", choices=item_choices)

    if not item_prompt:
        console.print("Thank you for visiting the Sandridge shop! See you next time!")
        return

    selected_item = item_choices[item_prompt]
    quantity = Prompt.ask("How many would you like?", type=int)

    if quantity <= selected_item.quantity:
        player_item = PlayerInventory(item_id=selected_item.item_id, quantity=quantity)
        session.add(player_item)
        session.commit()
        console.print(f"You have purchased {quantity} {selected_item.item.name}.")
    else:
        console.print("Sorry, the selected item is out of stock.")


def show_inventory():
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Item", style="cyan")
    table.add_column("Quantity", justify="right", style="green")

    inventory_items = session.query(PlayerInventory).join(FoodAndDrinks).all()

    if not inventory_items:
        console.print("Your inventory is empty.")
        return

    for item in inventory_items:
        table.add_row(item.item.name, str(item.quantity))

    console.print(table)


if __name__ == "__main__":
    console.print(Panel.fit("[bold]Welcome to the Sandridge Shop![/bold]", style="cyan"))

    while True:
        console.print("\n[bold]Main Menu[/bold]")
        console.print("[1] Enter the shop")
        console.print("[2] Check your inventory")
        console.print("[Q] Quit")

        choice = Prompt.ask("Please select an option:")

        if choice == "1":
            show_shop()
            buy_item()
        elif choice == "2":
            show_inventory()
        elif choice.lower() == "q":
            console.print("Thank you for using the Sandridge Shop. Goodbye!")
            break
        else:
            console.print("Invalid choice. Please try again.")
