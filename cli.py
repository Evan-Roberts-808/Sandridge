from pyfiglet import Figlet
from colorama import init, Fore, Style
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

white = "\033[0m"
ascii_bettys_diner = f"""{white}
                            ⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣶⣿⣿⣿⣿⣿⣿⠿⠷⣶⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣯⣀⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀
                            ⠀⠀⠀⢠⣿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣁⣈⣽⣿⣷⡀⠀⠀⠀
                            ⠀⠀⠀⣿⣿⣶⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⢿⣧⠀⠀⠀
                            ⠀⠀⠀⠛⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠧⠤⠾⠿⠿⠿⠿⠿⠷⠶⠾⠟⠀⠀⠀
                            ⠀⠀⠀⢶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⠶⠶⠀⠀⠀
                            ⠀⠀⣠⣤⣤⣤⣤⣤⣤⣄⣀⣀⣈⣉⣉⣉⣀⣀⣀⣀⣀⣠⣤⣤⣤⣤⣤⣄⠀⠀
                            ⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀
                            ⠀⠀⢀⣤⣭⠉⠉⠉⢉⣉⡉⠉⠉⠉⣉⣉⠉⠉⠉⢉⣉⠉⠉⠉⢉⣭⣄⠀⠀⠀
                            ⠀⠰⡟⠁⠈⢷⣤⣴⠟⠉⠻⣄⣠⡾⠋⠙⠳⣤⣴⠟⠉⠳⣦⣠⡾⠃⠙⢷⡄⠀
                            ⠀⠀⠀⢀⣀⣀⣉⡀⠀⠀⠀⠈⠉⠀⠀⠀⣀⣈⣁⣀⣀⣀⣀⣉⣀⣀⠀⠀⠀⠀
                            ⠀⠀⠀⠛⠛⠛⠛⠛⠛⠻⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠛⠛⠛⠛⠛⠛⠛⠃⠀⠀
                            ⠀⠀⠀⢸⣿⣿⣿⣿⣷⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀  
  _      __    __                     __         ___      __  __      _        ___  _             
 | | /| / /__ / /______  __ _  ___   / /____    / _ )___ / /_/ /___ _( )___   / _ \(_)__  ___ ____
 | |/ |/ / -_) / __/ _ \/  ' \/ -_) / __/ _ \  / _  / -_) __/ __/ // //(_-<  / // / / _ \/ -_) __/
 |__/|__/\__/_/\__/\___/_/_/_/\__/  \__/\___/ /____/\__/\__/\__/\_, / /___/ /____/_/_//_/\__/_/   
                                                               /___/                              
        """

ascii_oasis_fuel_n_go = f"""{white}

                                            ⠀⠈⠛⠻⠶⣶⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                            ⠀⠀⠀⠀⠀⠈⢻⣆⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀
                                            ⠀⠀⠀⠀⠀⠀⠀⢻⡏⠉⠉⠉⠉⢹⡏⠉⠉⠉⠉⣿⠉⠉⠉⠉⠉⣹⠇⠀⠀⠀
                                            ⠀⠀⠀⠀⠀⠀⠀⠈⣿⣀⣀⣀⣀⣸⣧⣀⣀⣀⣀⣿⣄⣀⣀⣀⣠⡿⠀⠀⠀⠀
                                            ⠀⠀⠀⠀⠀⠀⠀⠀⠸⣧⠀⠀⠀⢸⡇⠀⠀⠀⠀⣿⠁⠀⠀⠀⣿⠃⠀⠀⠀⠀
                                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣧⣤⣤⣼⣧⣤⣤⣤⣤⣿⣤⣤⣤⣼⡏⠀⠀⠀⠀⠀
                                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⠀⠀⢸⡇⠀⠀⠀⠀⣿⠀⠀⢠⡿⠀⠀⠀⠀⠀⠀
                                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣷⠤⠼⠷⠤⠤⠤⠤⠿⠦⠤⠾⠃⠀⠀⠀⠀⠀⠀
                                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢾⣷⢶⣶⠶⠶⠶⠶⠶⠶⣶⠶⣶⡶⠀⠀⠀⠀⠀⠀⠀
                                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣧⣠⡿⠀⠀⠀⠀⠀⠀⢷⣄⣼⠇⠀⠀⠀⠀⠀⠀⠀

  /$$$$$$                      /$$                 /$$$$$$$$                  /$$                        /$$$$$$           
 /$$__  $$                    |__/                | $$_____/                 | $$                       /$$__  $$          
| $$  \ $$  /$$$$$$   /$$$$$$$ /$$  /$$$$$$$      | $$    /$$   /$$  /$$$$$$ | $$       /$$$$$$$       | $$  \__/  /$$$$$$ 
| $$  | $$ |____  $$ /$$_____/| $$ /$$_____/      | $$$$$| $$  | $$ /$$__  $$| $$      | $$__  $$      | $$ /$$$$ /$$__  $$
| $$  | $$  /$$$$$$$|  $$$$$$ | $$|  $$$$$$       | $$__/| $$  | $$| $$$$$$$$| $$      | $$  \ $$      | $$|_  $$| $$  \ $$
| $$  | $$ /$$__  $$ \____  $$| $$ \____  $$      | $$   | $$  | $$| $$_____/| $$      | $$  | $$      | $$  \ $$| $$  | $$
|  $$$$$$/|  $$$$$$$ /$$$$$$$/| $$ /$$$$$$$/      | $$   |  $$$$$$/|  $$$$$$$| $$      | $$  | $$      |  $$$$$$/|  $$$$$$/
 \______/  \_______/|_______/ |__/|_______/       |__/    \______/  \_______/|__/      |__/  |__/       \______/  \______/ 
                                                                                                                                                                                                                                                                                                                                                                  
"""


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
        food_and_drinks = session.query(FoodAndDrinks).all() #pulls data from FoodAndDrinks table and assigns it to food_and_drinks variable

        # this defines the location ID for each item based on its location
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

        for item in food_and_drinks: #iterates over each item in food_and_drinks
            existing_item = session.query( #checks item.id to see whether or not its already in the shop_inventory table
                ShopInventory).filter_by(item_id=item.id).first()
            if not existing_item: #if it isnt already in the shop_inventory table create a new object and commit it to the table
                location_id = location_ids.get(item.name.lower()) # Assign the location ID based on the item's name
                if location_id:
                    shop_item = ShopInventory(
                        item_id=item.id, price=item.price, quantity=10, location_id=location_id)
                    session.add(shop_item)
        session.commit()

    def select_location(self):
        self.console.print("[bold]Select Location[/bold]")
        locations = session.query(Location).all() #queries from the locations table and assigns data to locations variable
        location_choices = {
            str(location.id): location for location in locations} #creates a dict of locations id

        for i, location in enumerate(locations, start=1): #loops over locations and enumerates them to obtain an index for each lcoation starting at 1 to use for location selection
            self.console.print(f"{i}. {location.name}")
            location_choices[str(i)] = location

        location_prompt = Prompt.ask(
            "Please select a location:", choices=location_choices) #creates prompt to ask for which location youd like to go to

        if location_prompt in location_choices: #checks if the answer to the prompt is within the choices, if it is sets the location to the selected one
            self.current_location = location_choices[location_prompt]
            self.choices = self.location_choices

            if self.current_location.name == "Bettys Diner": #depending on which selection is made prints corresponding ASCII art
                self.console.print(ascii_bettys_diner)
            if self.current_location.name == "Oasis Fuel n Go":
                self.console.print(ascii_oasis_fuel_n_go)
        else:
            self.console.print("Invalid location. Please try again.") #if valid location isnt selected prints invaled location

    def view_shop(self):
        self.console.print("[bold]Shop Inventory[/bold]")
        #creates table that gets printing into the terminal to view what is in the shop
        table = Table(title="Shop Inventory",
                      show_header=True, header_style="bold")
        table.add_column("ID", justify="right")
        table.add_column("Item")
        table.add_column("Price", justify="right")
        table.add_column("Quantity", justify="right")

        shop_items = session.query(ShopInventory).join(FoodAndDrinks).filter( #queries to ShopInvetory table and filters the items within by the location id key
            ShopInventory.location_id == self.current_location.id).all()

        if not shop_items: #if the shop has nothing for sale display out of stock
            self.console.print(
                "The shop is currently out of stock. Please check back later.")
            return

        for item in shop_items: #iterates over filtered items to add rows to table that is being printed
            table.add_row(str(item.item_id), item.item.name,
                          str(item.price), str(item.quantity))

        self.console.print(table) #prints table

    def show_player_inventory(self):
        self.console.print("[bold]Player Inventory[/bold]")
        #creates table to be printed using the player inventory
        table = Table(title="Player Inventory",
                      show_header=True, header_style="bold")
        table.add_column("ID", justify="right")
        table.add_column("Item")
        table.add_column("Quantity", justify="right")

        inventory_items = session.query( #queries from the PlayerInventory table to get items and assign it to inventory_items variable
            PlayerInventory).join(FoodAndDrinks).all()

        if not inventory_items: #checks if you have no items and prints to tell you accordingly
            self.console.print("Your inventory is empty.")
            return

        for item in inventory_items: #iterates over inventory_items and adds a row to the printed table for each
            table.add_row(str(item.item_id), item.item.name,
                          str(item.quantity))

        self.console.print(table) #prints the table

    def buy_item(self):
        self.console.print("[bold]Buy Item[/bold]")
        shop_items = session.query(ShopInventory).join(FoodAndDrinks).filter( #queries the ShopInventory table and filters by location to fill the shop_items variable accordingly
            ShopInventory.location_id == self.current_location.id).all()

        if not shop_items: #if theres no items say out of stock
            self.console.print(
                "The shop is currently out of stock. Please check back later.")
            return

        item_choices = {}
        for item in shop_items: # iterate over each item to create a choice for each
            item_choices[str(item.item_id)] = item

        item_prompt = Prompt.ask(
            "Can you enter the ID of the item you want to purchase?:", choices=item_choices) #prompts the user to ask for an item by id

        if not item_prompt: # if no item prompt thanks them for visiting
            self.console.print(
                "Thank you for visiting the Sandridge shop! See you next time!")
            return

        selected_item = item_choices[item_prompt] # assigns selected item to selected_item variable
        quantity = int(Prompt.ask("Great! How many would you like to buy?:")) #asks for a quantity amount 

        if selected_item.quantity >= quantity: # checks if theres enough quantity to buy if there is add the item to the player inventory
            total_cost = selected_item.price * quantity
            player_item = session.query(PlayerInventory).filter_by(
                item_id=selected_item.item_id).first()
            if player_item:
                player_item.quantity += quantity
            else:
                player_item = PlayerInventory(
                    item_id=selected_item.item_id, quantity=quantity)
                session.add(player_item)

            selected_item.quantity -= quantity #subtracts selected quantity from shop quantity
            session.commit()

            self.console.print( #prints message thanking them
                f"You have successfully purchased {quantity} {selected_item.item.name}(s) for a total cost of {total_cost}."
            )
        else:
            self.console.print( #tells user not enough in stock
                f"Sorry, there is not enough stock for {quantity} {selected_item.item.name}(s). Please try again later."
            )

    def quit(self): #quits the cli if quit is called
        self.console.print(
            "Thank you for visiting the Sandridge! See you next time!")
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
        self.console.print("Welcome to the Sandridge!")
        self.console.print("Please select an option:")
        while True:
            self.console.print("[bold]Main Menu[/bold]")
            self.console.print("1. Select Location")
            self.console.print("2. Show Player Inventory")
            if self.current_location:
                self.console.print("3. View Shop Inventory")
                self.console.print("4. Buy Item")
            self.console.print("q. Quit")

            choice = Prompt.ask(
                "What would you like to do?", choices=self.choices)

            action = self.choices.get(choice)
            if action:
                action()
            else:
                self.console.print("Invalid choice. Please try again.")


if __name__ == "__main__":
    cli = CLI()
    cli.restock_shop()
    cli.run()
