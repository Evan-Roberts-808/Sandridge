from pyfiglet import Figlet
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.db.models import FoodAndDrinks, PlayerInventory, ShopInventory, Location
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
            "1": self.select_location,
            "2": self.show_player_inventory,
            "q": self.quit
        }
        self.location_choices = {
            "1": self.select_location,
            "3": self.view_shop,
            "2": self.show_player_inventory,
            "4": self.buy_item,
            "q": self.quit
        }
        self.current_location = None

    def restock_shop(self):
        food_and_drinks = session.query(FoodAndDrinks).all()

        # this should define the location ID for each item based on its location
        location_ids = {
            'cheeseburger': 1,
            'pancake': 1,
            'milkshake': 1,
            'french fries': 1,
            'candy bar': 2,
            'beef jerky': 2,
            'energy drink': 2,
            'bag of chips': 2,
            'bottled water': 2,
            'fruit salad cup': 2,
            'granola bar': 2,
            'protein shake': 2,
        }

        for item in food_and_drinks:
            existing_item = session.query(
                ShopInventory).filter_by(item_id=item.id).first()
            if not existing_item:
                # Assign the location ID based on the item's name
                location_id = location_ids.get(item.name.lower())
                if location_id:
                    shop_item = ShopInventory(
                        item_id=item.id, price=item.price, quantity=10, location_id=location_id)
                    session.add(shop_item)
        session.commit()

    def select_location(self):
        self.console.print("[bold]Select Location[/bold]")
        locations = session.query(Location).all()
        location_choices = {
            str(location.id): location for location in locations}

        for i, location in enumerate(locations, start=1):
            self.console.print(f"{i}. {location.name}")
            location_choices[str(i)] = location

        location_prompt = Prompt.ask(
            "Please select a location:", choices=location_choices)

        if location_prompt in location_choices:
            self.current_location = location_choices[location_prompt]
            self.choices = self.location_choices
        else:
            self.console.print("Invalid location. Please try again.")

    def view_shop(self):
        self.console.print("[bold]Shop Inventory[/bold]")
        table = Table(title="Shop Inventory",
                      show_header=True, header_style="bold")
        table.add_column("ID", justify="right")
        table.add_column("Item")
        table.add_column("Price", justify="right")
        table.add_column("Quantity", justify="right")

        shop_items = session.query(ShopInventory).join(FoodAndDrinks).filter(
            ShopInventory.location_id == self.current_location.id).all()

        if not shop_items:
            self.console.print(
                "The shop is currently out of stock. Please check back later.")
            return

        for item in shop_items:
            table.add_row(str(item.item_id), item.item.name,
                          str(item.price), str(item.quantity))

        self.console.print(table)

    def show_player_inventory(self):
        self.console.print("[bold]Player Inventory[/bold]")
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

    def buy_item(self):
        self.console.print("[bold]Buy Item[/bold]")
        shop_items = session.query(ShopInventory).join(FoodAndDrinks).filter(
            ShopInventory.location_id == self.current_location.id).all()

        if not shop_items:
            self.console.print(
                "The shop is currently out of stock. Please check back later.")
            return

        item_choices = {}
        for item in shop_items:
            item_choices[str(item.item_id)] = item

        item_prompt = Prompt.ask(
            "Can you enter the ID of the item you want to purchase?:", choices=item_choices)

        if not item_prompt:
            self.console.print(
                "Thank you for visiting the Sandridge shop! See you next time!")
            return

        selected_item = item_choices[item_prompt]
        quantity = int(Prompt.ask("Great! How many of those would you like?"))

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

    def quit(self):
        self.console.print(
            "Thank you for visiting the Sandridge shop! See you next time!")
        raise SystemExit

    def run(self):
        ascii_art = """
            
  sSSs   .S_SSSs     .S_sSSs     .S_sSSs     .S_sSSs     .S   .S_sSSs      sSSSSs    sSSs  
 d%%SP  .SS~SSSSS   .SS~YS%%b   .SS~YS%%b   .SS~YS%%b   .SS  .SS~YS%%b    d%%%%SP   d%%SP  
d%S'    S%S   SSSS  S%S   `S%b  S%S   `S%b  S%S   `S%b  S%S  S%S   `S%b  d%S'      d%S'    
S%|     S%S    S%S  S%S    S%S  S%S    S%S  S%S    S%S  S%S  S%S    S%S  S%S       S%S     
S&S     S%S SSSS%S  S%S    S&S  S%S    S&S  S%S    d*S  S&S  S%S    S&S  S&S       S&S     
Y&Ss    S&S  SSS%S  S&S    S&S  S&S    S&S  S&S   .S*S  S&S  S&S    S&S  S&S       S&S_Ss  
`S&&S   S&S    S&S  S&S    S&S  S&S    S&S  S&S_sdSSS   S&S  S&S    S&S  S&S       S&S~SP  
  `S*S  S&S    S&S  S&S    S&S  S&S    S&S  S&S~YSY%b   S&S  S&S    S&S  S&S sSSs  S&S     
   l*S  S*S    S&S  S*S    S*S  S*S    d*S  S*S   `S%b  S*S  S*S    d*S  S*b `S%%  S*b     
  .S*P  S*S    S*S  S*S    S*S  S*S   .S*S  S*S    S%S  S*S  S*S   .S*S  S*S   S%  S*S.    
sSS*S   S*S    S*S  S*S    S*S  S*S_sdSSS   S*S    S&S  S*S  S*S_sdSSS    SS_sSSS   SSSbs  
YSS'    SSS    S*S  S*S    SSS  SSS~YSSY    S*S    SSS  S*S  SSS~YSSY      Y~YSSY    YSSP  
               SP   SP                      SP          SP                                 
               Y    Y                       Y           Y                                  
                                                                                           

        """
        self.console.print(ascii_art)
        self.console.print("Welcome to the Sandridge shop!")
        self.console.print("Please select an option:")
        while True:
            self.console.print("[bold]Main Menu[/bold]")
            self.console.print("1. Select Location")
            self.console.print("2. Show Player Inventory")
            if self.current_location:
                self.console.print("3. View Shop Inventory")
                self.console.print("4. Buy Item")
            self.console.print("q. Quit")

            choice = Prompt.ask("What would you like to do?", choices=self.choices)

            action = self.choices.get(choice)
            if action:
                action()
            else:
                self.console.print("Invalid choice. Please try again.")


if __name__ == "__main__":
    cli = CLI()
    cli.restock_shop()
    cli.run()
