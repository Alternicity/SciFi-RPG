#weapons.py split from InWorldObject to shorten file sizes

from InWorldObjects import ObjectInWorld, Size, Toughness


valid_items = [
    "Pistol", "SMG", "Rifle", "Shotgun", 
    "Sword", "Knife", "Club", "Electrobaton"
]

#Weapon is also an abstract class, then attributes like damage_points and legality should indeed be defined 
#at the level of the most specific concrete classes that directly need them
class Weapon(ObjectInWorld):
    is_concrete = False  # An abstract class
    def __init__(self, name, toughness, value, size, damage,):
        super().__init__(name, toughness, value, item_type="weapon")
        self.size = size

#RangedWeapon is also an abstract class, then attributes like damage_points and legality should indeed be defined 
#at the level of the most specific concrete classes that directly need them
class RangedWeapon(Weapon):
    is_concrete = False  # An abstract class
    def __init__(self, name, toughness, value, size, damage, ammo, range):
        super().__init__(name, toughness, value, size, damage)
        self.range = range # Common attribute for all ranged weapons



#MeleeWeapon is also an abstract class, then attributes like damage_points and legality should indeed be defined 
#at the level of the most specific concrete classes that directly need them
class MeleeWeapon(Weapon):
    is_concrete = False  # An abstract class
    def __init__(self, name, toughness, value, size, damage):
        super().__init__(name, toughness, value, size, damage)

#only concrete, fully implementable classes have the damage_points
#and legality attributes.
#Any object that represents something that could potentially break or
#degrade over time should have damage_points.
#Weapons will need both damage (the amount of 
#damage they deal in combat) and damage_points

class Pistol(RangedWeapon):
    is_concrete = True  # A concrete class will create objects and have more attributes
    def __init__(self, value=100, ammo=12, legality=True): 
        super().__init__(
            name="Pistol",
            toughness=Toughness.NORMAL,
            value=value,
            damage=10,  # Damage for the Pistol
            size=Size.ONE_HANDED,  # size is now passed here
            ammo=12,
            range=50
        )
        self.value = value
        self.legality = legality
        self.item_type = "weapon"
        range=50,



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
        )
        self.blackmarket_value = 500  # Set blackmarket_value directly in SMG
        self.item_type = "weapon"

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
        )
        self.value = value
        self.legality = legality
        self.item_type = "weapon"

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
        )
        self.value = value
        self.legality = legality
        self.item_type = "weapon"

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
        )
        self.value = value
        self.legality = legality
        self.item_type = "weapon"

class Knife(MeleeWeapon):
    is_concrete = True  # An concrete class will create objects and have more attributes
    def __init__(self, value=50, legality=True):
        super().__init__(
            name="Knife",
            toughness=Toughness.DURABLE,
            legality=legality,
            value=value,
            size=Size.ONE_HANDED,  # size is now passed here
            damage=8,  # Damage for the Knife
        )
        self.value = value
        self.legality = legality
        self.item_type = "weapon"

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
            charge=0, # not used by this object, delete?
        )
        self.value = value
        self.legality = legality
        self.item_type = "weapon"

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
        )
        self.value = value
        self.legality = legality
        self.item_type = "weapon"