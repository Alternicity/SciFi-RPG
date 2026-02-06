import os
import json
import display


class Loyalty:
    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.loyalties = {}

    def add_loyalty(self, faction_name, value):
        self.loyalties[faction_name] = value

    def display_loyalties(self):
        return self.loyalties

    def save_loyalty(self):
        # Specify the directory to save loyalty data
        base_path = f"data/loyalties/{self.entity_id}"

        # Ensure the directory exists
        os.makedirs(base_path, exist_ok=True)

        # Define the file path for saving the loyalty data
        file_path = os.path.join(base_path, "loyalty_data.json")

        # Save the loyalty data as a JSON file
        with open(file_path, "w") as file:
            json.dump(self.loyalties, file)
        print(f"Loyalty data saved to {file_path}")

    def load_loyalty(self):
        # Specify the directory where loyalty data is saved
        base_path = f"data/loyalty/{self.entity_id}"


        # Define the file path for loading the loyalty data
        file_path = os.path.join(base_path, "loyalty.json")


        # Load the loyalty data if the file exists
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                self.loyalties = json.load(file)
            print(f"Loyalty data loaded from {file_path}")
        else:
            print(f"No loyalty data found for {self.entity_id}")


class LoyaltySystem:
    def __init__(self, region_name):
        self.region_name = region_name
        self.characters = {}

    def add_character(self, character):
        if isinstance(
            character, Character
        ):  # Optional check to ensure it's a Character
            self.characters[character.entity_id] = character
        else:
            print(f"Error: Invalid character passed - {character}")

    def get_loyalty(self, character_id):
        if character_id in self.characters:
            return self.characters[character_id].loyalties
        else:
            print(f"Character with ID {character_id} not found.")
            return None


def test_loyalty_system(character):
    #Actions that a faction or character asks another character to take have a risk value
    #If that characters loyalty exceeds that risk, they willl make the attempt
    #If they succeed in taht task, their loyalty may increase and they will receive
    #A a status buff.

def divided loyalty(character)
    #If a character has a loyalty to  acharacter or a faction AND a loyalty to a rival
    #character or faction then they have a divided loyalty.

    #There needs to be a function for them to pick a side, if a situation demands it.
    #One loyalty can become part of a hidden identity/loyalty.

def hidden_loyalty
    #some characters may be spies or traitors or assassin's an pretend to have loyalty to a give entity
    #but really are loyalty to another, or to a motive like profit

def group mentality
    #most characters give their loyalty to the same entities or character that their loved ones do

def love()
    #Characters may have a love loyalty which might cause the to PROACTIVLY attempt to help
    #their loved ones, especially feed the and give gifts

def erodeLoyalty()
    #Sometimes an event can erode loyalties, for instance a psyop news event or badOptics outcome froma misssion

def gainLoyalty()
    #Sometimes a character can attempt to gain anothers loyalty, eith for themselves, or a faction.
    #Feeding a character helps, especially if they are very hungry


def convince()
    #Sometimes a character will try to convince another that a certain idea or ideology is correct.
    An attempt is made, a typical RPG test of skill (random number vs athe characters intelligence +charisma /2)
    #And if it succeeds the recipient gets a resist attempt (random number gen vs their int + somethign /2)
    #If a charcter becomes convinced they may also become VeryCanvinced and proclaim their new
    #belief, and try to convince other characters as well.

