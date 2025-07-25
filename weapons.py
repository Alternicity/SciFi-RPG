#weapons.py split from InWorldObject to shorten file sizes

from InWorldObjects import ObjectInWorld, Size, Toughness
import logging

valid_items = [
    "Pistol", "SMG", "Rifle", "Shotgun", 
    "Sword", "Knife", "Club", "Electrobaton"
]

#Weapon is also an abstract class, then attributes like damage_points and legality should indeed be defined 
#at the level of the most specific concrete classes that directly need them
class Weapon(ObjectInWorld):
    is_concrete = False
    def __init__(self, name, toughness, price, size, blackmarket_value, damage_points, legality, damage, owner_name=None, intimidation=1):
        super().__init__(name=name, toughness=toughness, item_type="Weapon", size=size, blackmarket_value=blackmarket_value, price=price, damage_points=damage_points, legality=legality, owner_name=owner_name)
        self.damage = damage
        self.intimidation = intimidation  # Base intimidation factor
        self.name = name
        self.owner = owner_name      # Original or legal owner
        self.user = None        # Currently wielding the weapon
        self.history = []  # List of (character, event_type, timestamp)

    @property
    def tags(self):
        return super().tags + ["weapon"]

    def assign_user(self, character):
        self.user = character
        logging.info(f"{character.name} is now using {self.name}")

    def change_ownership(self, new_owner):
        self.owner = new_owner
        logging.info(f"{self.name} is now owned by {new_owner.name}")
        #switch to prints at some point?

#RangedWeapon is also an abstract class, then attributes like damage_points and legality should indeed be defined 
#at the level of the most specific concrete classes that directly need them
class RangedWeapon(Weapon):
    is_concrete = False
    def __init__(self, name, toughness, price, size, blackmarket_value, damage_points, legality, damage, range, ammo, intimidation=3):
        super().__init__(name=name, toughness=toughness, price=price, size=size, blackmarket_value=blackmarket_value, damage_points=damage_points, legality=legality, damage=damage, intimidation=intimidation)
        self.range = range
        self.ammo = ammo

    @property
    def tags(self):
        return super().tags + ["ranged", "ranged_weapon"]
#MeleeWeapon is also an abstract class, then attributes like damage_points and legality should indeed be defined 
#at the level of the most specific concrete classes that directly need them
class MeleeWeapon(Weapon):
    is_concrete = False
    def __init__(self, name, toughness, price, size, damage, blackmarket_value=50, damage_points=10, legality=True, owner_name=None, intimidation=2):
        super().__init__(name=name, toughness=toughness, price=price, size=size, blackmarket_value=blackmarket_value, damage_points=damage_points, legality=legality, owner_name=owner_name, damage=damage, intimidation=intimidation)

#only concrete, fully implementable classes have the damage_points
#and legality attributes.
#Any object that represents something that could potentially break or
#degrade over time should have damage_points.
#Weapons will need both damage (the amount of 
#damage they deal in combat) and damage_points

class Pistol(RangedWeapon):
    is_concrete = True
    def __init__(self, price=500, quantity=1, ammo=12, legality=True): 
        super().__init__(
            name="Pistol",
            toughness=Toughness.NORMAL,
            price=price,
            size=Size.ONE_HANDED,
            blackmarket_value=150,
            damage_points=10,
            legality=legality,
            damage=10,
            range=50,
            ammo=ammo,
            intimidation=7
        )
        self.owner_name = None
        self.human_readable_id = "Unowned Pistol"

    def get_percept_data(self, observer=None):
        data = {
            "description": self.human_readable_id or "Pistol",
            "type": self.__class__.__name__,
            "origin": self,
            "urgency": 1,
            "source": None,
            "tags": self.tags,
            "size": getattr(self, "size", None),
        }

        return data

    @property
    def tags(self):
        return super().tags + ["pistol", "weapon", "ranged", "ranged_weapon"]
        #does this need to be called for pistol instances to have tags?
    
        
    
    
#You can abstract this into a helper method later, but this is a good explicit start.
#This allows the object to generate percepts from the perspective of the observer.

class SMG(RangedWeapon):
    is_concrete = True  # An concrete class will create objects and have more attributes
    def __init__(self):
        # Pass the right parameters to the parent constructor
        super().__init__(
            name="SMG",
            toughness=Toughness.NORMAL,
            damage_points=15,
            legality=False,
            value=250,
            size=Size.TWO_HANDED,
            damage=25,
            ammo=30,
            range=50,
            intimidation=10
        )
        self.blackmarket_value = 500  # Set blackmarket_value directly in SMG
        self.item_type = "weapon"

    def get_percept_data(self, observer=None):
        tags = ["weapon", "SMG", "ranged"]
        return {
            "description": f"{self.name}",
            "type": self.__class__.__name__,
            "origin": self,
            "item_type": self.item_type,
            "value": self.price,
            "tags": tags,
            "danger": self.intimidation,
            "size": self.size.value if hasattr(self, "size") else None
        }
    
class Rifle(RangedWeapon):
    is_concrete = True  # An concrete class will create objects and have more attributes
    def __init__(self, value=200, legality=True):
        super().__init__(
            name="Rifle",
            toughness=Toughness.NORMAL,
            legality=legality,
            value=value,
            size=Size.TWO_HANDED,  # size is now passed here
            damage=25,  # Damage for the Rifle
            ammo=30,
            charge=0,
            range=200,
            intimidation=13
        )
        self.value = value
        self.legality = legality
        self.item_type = "weapon"

    def get_percept_data(self, observer=None):
        tags = ["weapon", "rifle", "ranged"]
        return {
            "description": f"{self.name}",
            "type": self.__class__.__name__,
            "origin": self,
            "item_type": self.item_type,
            "value": self.price,
            "tags": tags,
            "danger": self.intimidation,
            "size": self.size.value if hasattr(self, "size") else None
        }

class Shotgun(RangedWeapon):
    is_concrete = True  # An concrete class will create objects and have more attributes
    def __init__(self, value=250, legality=True):
        super().__init__(
            name="Shotgun",
            toughness=Toughness.NORMAL,
            legality=legality,
            value=value,
            size=Size.TWO_HANDED,  # size is now passed here
            damage=30,  # Damage for the Shotgun
            ammo=8,
            charge=0,
            range=40,
            intimidation=13
        )
        self.value = value
        self.legality = legality
        self.item_type = "weapon"

    def get_percept_data(self, observer=None):
        tags = ["weapon", "shotgun", "ranged"]
        return {
            "description": f"{self.name}",
            "type": self.__class__.__name__,
            "origin": self,
            "item_type": self.item_type,
            "value": self.price,
            tags: tags,
            "danger": self.intimidation,
            "size": self.size.value if hasattr(self, "size") else None
        }

class Sword(MeleeWeapon):
    is_concrete = True  # An concrete class will create objects and have more attributes
    def __init__(self, value=150, legality=True):
        super().__init__(
            name="Sword",
            toughness=Toughness.DURABLE,
            legality=legality,
            value=value,
            size=Size.ONE_HANDED,  # size is now passed here
            damage=15,  # Damage for the Sword
            charge=0,
            intimidation=4
        )
        self.value = value
        self.legality = legality
        self.item_type = "weapon"

    def get_percept_data(self, observer=None):
        tags = ["weapon", "sword"]
        return {
            "description": f"{self.name}",
            "type": self.__class__.__name__,
            "origin": self,
            "item_type": self.item_type,
            "value": self.price,
            "danger": self.intimidation,
            "size": self.size.value if hasattr(self, "size") else None
        }

class Knife(MeleeWeapon):
    is_concrete = True  # An concrete class will create objects and have more attributes
    def __init__(self, price=50, legality=True, owner_name=None):
        super().__init__(
            name="Knife",
            toughness=Toughness.DURABLE,
            price=price,
            size=Size.ONE_HANDED,  # size is now passed here
            damage=8,  # Damage for the Knife
            blackmarket_value=30,
            damage_points=5,
            legality=legality,
            owner_name=owner_name,
            intimidation=3
        )
        self.price = price
        self.legality = legality
        self.item_type = "weapon"
        self.human_readable_id = f"{owner_name}'s Knife" if owner_name else "Unowned Knife"
    
    def get_percept_data(self, observer=None):
        tags = ["weapon", "knife"]
        return {
            "description": f"Knife ({self.human_readable_id})",
            "type": self.__class__.__name__,
            "origin": self,
            "value": self.price,
            "danger": self.intimidation,
            "item_type": self.item_type,
            "size": self.size.value if hasattr(self, "size") else None
        }

class Club(MeleeWeapon):
    is_concrete = True  # An concrete class will create objects and have more attributes
    def __init__(self, value=70, legality=True):
        super().__init__(
            name="Club",
            toughness=Toughness.DURABLE,
            legality=legality,
            value=value,
            size=Size.ONE_HANDED,  # size is now passed here
            damage=12,  # Damage for the Club
            intimidation=3
        )
        self.value = value
        self.legality = legality
        self.item_type = "weapon"

    def get_percept_data(self, observer=None):
        tags = ["weapon", "club"]
        return {
            "description": f"{self.name}",
            "type": self.__class__.__name__,
            "origin": self,
            "item_type": self.item_type,
            "value": self.price,
            "danger": self.intimidation,
            "size": self.size.value if hasattr(self, "size") else None
        }


class Electrobaton(MeleeWeapon):
    is_concrete = True  # An concrete class will create objects and have more attributes
    def __init__(self, value=70, legality=True):
        super().__init__(
            name="Electrobaton",
            toughness=Toughness.DURABLE,
            legality=legality,
            value=value,
            size=Size.ONE_HANDED,  # size is now passed here
            damage=12,  # Damage for the Club
            charge=0,
            intimidation=5
        )
        self.value = value
        self.legality = legality
        self.item_type = "weapon"

    def get_percept_data(self, observer=None):
        tags = ["weapon", "electrobaton"]
        return {
            "description": f"{self.name}",
            "type": self.__class__.__name__,
            "origin": self,
            "item_type": self.item_type,
            "value": self.price,
            "danger": self.intimidation,
            "size": self.size.value if hasattr(self, "size") else None
        }