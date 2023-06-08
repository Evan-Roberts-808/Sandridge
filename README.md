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

