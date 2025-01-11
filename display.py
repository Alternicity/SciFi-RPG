from tabulate import tabulate
from characters import Character
import logging
import time
from utils import list_characters
from character_creation import create_characters_as_objects

def display_menu():
    """
    Displays the main menu and handles user choices.
    """
    characters = []  # Initialize as an empty list for later use

    while True:
        print("\n=== Main Menu ===")
        print("1: Create Characters (Game Objects)")
        print("2: Create Characters (Serialized Data)")
        print("3: Load Serialized Characters")
        print("4: Play/Test Game")
        print("5: Exit")

        choice = input("Enter your choice: ")
        try:
            choice = int(choice)
            if choice == 1:
                # Create characters as objects
                characters = create_characters_as_objects()  # Now doesn't require list_characters
                print("\n=== Character Information ===")
                print(list_characters(characters))  # Call list_characters separately
            elif choice == 2:
                # Placeholder for serialization feature
                print("Feature to create and serialize characters is under development.")
            elif choice == 3:
                # Placeholder for loading serialized data
                print("Feature to load serialized characters is under development.")
            elif choice == 4:
                # Placeholder for game/test logic
                if characters:
                    print("Starting game with current characters...")
                else:
                    print("No characters created yet. Please create characters first.")
            elif choice == 5:
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid choice. Please select a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number.")
            time.sleep(1)



if __name__ == "__main__":
    characters = []  # Initialize characters list
    display_menu(characters)
