from inventory import Inventory
from characters import Character

class Player(Character):
    def __init__(self, name, health = 100):
        self.name = name
        self.health = health
        self.inventory = Inventory()
        self.faction = None
        
    def join_faction(self, faction):
        self.faction = faction
        print(f"{self.name} joined {faction.name}")
        
    def show_inventory(self):
        self.inventory.display_items()
        
    def take_damage(self, damage):

        print(f"{self.name} now has {self.health}")
        
    def interact_with_object(self, game_object):
        # example of player specific behaviour
        print(f"{self.name} interacts with {game_object.name}")