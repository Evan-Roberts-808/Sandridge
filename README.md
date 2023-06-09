#################################################################
![image](https://github.com/Evan-Roberts-808/Sandridge/assets/105817690/f4f35e90-f2b8-4ecc-a29e-13dee1784fcd)
#################################################################

Sandridge is a **in-development** command line text adventure. Below you can see our Roadmap to see which functionalities are currently built.

## Roadmap

- ~~Build shop functionality~~
    - ~~Have both the diner and convenience stores appearing at their appropriate location~~
    - ~~Have functionality to view the shop and purchase items and have them added to your inventory~~
- Add the rest of the locations
  - Town Hall, Motel Oasis, Abandoned Mine, Town Square, Library, Radio Station, Community Center, Old Windmill Farm, Local School
- NPCs and Dialogue
    - Create NPC table, Dialogue Table, and any necessary intermediary tables
    - Have NPCs be present at required locations
    - Implement dialogue system in the interface
- Quest and Objective
- Character set-up
    - Create character table, class table, ability table, and any necessary intermediary tables
    - Implement functionality for user to choose a class when creating character and link player_inventory to character
- Combat System
    - Create enemy table, and enemy_abilities intermediary table
    - Build out combat system methods and create methods to properly start combat
- Character Progression
    - Implement leveling system
    - Define XP requirements for each level
    - Implement ability unlocks on level based on character class
    - Implement character stat updates based on level
- Save State
    - Implement ability to resume on a created character or restart with a new and properly track progress across all
- Overall Testing
    - Proper balancing of combat and abilties, etc.

---

## Usage

To install and run, follow these steps:
1. Clone the repository
``` 
git@github.com:Evan-Roberts-808/Sandridge.git 
```
2. Navigate to the project directory:
```
cd relative/path/to/sandridge
```
3. Install the required dependencies and enter python shell:
```
pipenv install && pipenv shell
```
4. Run the CLI:
```
python cli.py
```
---
## Functions

**run**: The run function displays an ASCII art of the projects titled followed by a message and prompts for the user to input in order to call other functions.
- 1 Select location
- 2 Show player inventory
- q quit

Once a location is selected the prompts will change to display the following:
- 1 Select Location
- 2 Show player inventory
- 3 View shop
- 4 Buy item
- q quit

**restock_shop**: The restock_shop function pulls data from our food_and_drinks table and adds it to the shop_inventory table along with the quantity and location id required to filter the shops by which shop is selected by the user. It also acts as a way of preventing the shop_inventory from receiving duplicate items by checking whether or not they are already within the shop_inventory table.

**select_location**: The select_location function prompts the user to select from a list of locations and on choice will display a corresponding ASCII art for that location. This will also filter the shop_inventory by whichever location is selected.

**show_player_inventory**: The show_player_inventory function creates a table using rich with data queried from the PlayerInventory table. If the table is empty, it'll display a message letting you know the inventory is empty.

**view_shop**: The view_shop function creates a table using rich with data queried from the ShopInventory table. This queried data is filtered by location id based on which location is selected.

**buy_item**: The buy_item function prompts the user to enter an id from the current shop they are viewing along with a quantity, this is then subtracted from the shop quantity and added to the player_inventory table accordingly.

**quit**: The quit function displays a thank you message to the user then raises a SystemExit event to end the CLI.
