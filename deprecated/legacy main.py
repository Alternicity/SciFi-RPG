from loader import load_data
from object_factory import create_object
from faction import Faction, Corporation, Gang
from store import Dealer, CorporateDepot, Stash, Vendor
from inventory import Inventory
from InWorldObjects import ObjectInWorld
from characters import Character, Boss, Captain, Grunt, CEO, Manager, Employee
from common import Status


def main():
    Print("Welcome to the Test Menu")
    while True:
        print("\nChoose an option:")
        print("1. Display all factions data")
        print("2. Display state data")
        print("3. Test loyalty system (create, update, save, load)")
        print("4. Quit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            # Load and display factions data
            factions_data = load_data("data/factions.json")
            print("Factions data:")
            for faction in factions_data:
                print(faction)
                
        elif choice == "2":
            # Load and display state data
            state_data = load_data("data/state.json")
            print("State data:")
            print(state_data)
            
        elif choice == "3":
            # Test loyalty system
            entity_id = input("Enter an entity ID:")
            loyalty = Loyalty(entity_id)
            
            # Add some test loyalties
            loyalty.add_loyalty("FactionA", 80)
            loyalty.add_loyalty("FactionB", 60)
            print("Current loyalties:", loyalty.display_loyalties())
            
            #save loyalty data
            loyalty.save_loyalty()
            print(f"Loyalty data for {entity_id} saved.")
            
            #load loyalty data
            loyalty.load_loyalty()
            print(f"Loyalty data for {entity_id} loaded:", loyalty.display_loyalties())
            
        elif choice =="4"
            print("Exiting the test menu. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            
            if __name__ == "__main__":
    main()

# File paths for your data files
factions_file = "data/factions.yaml"
items_file = "data/items.json"

# Load data
factions_data = load_data(factions_file)
items_data = load_data(items_file)

items = [create_object(data) for data in items_data]

# Example gang faction
red_gang = Faction(name = "Red Gang", type="gang")

# Create members
red_boss = Boss(name="Big Red", faction="Red Gang")
captain_1 = Captain(name="Red Captain 1", faction="Red Gang")
grunt_1 = Grunt(name="Red Grunt 1", faction="Red Gang")
grunt_2 = Grunt(name="Red Grunt 2", faction="Red Gang")

# Add members to Red Gang
red_gang.add_member(red_boss)
red_gang.add_member(captain_1)
red_gang.add_member(grunt_1)
red_gang.add_member(grunt_2)


# Boss sets a faction goal
red_gang.set_goal("expand_territory")
red_gang.display_goal()


# Captain adds and delegates tasks
captain_1.add_task("Patrol Sector A") # Capitalize "Sector A" consistently
captain_1.delegate_task("Patrol sector A", [grunt_1, grunt_2])

# Print Red Gang hierarchy
print(f"{red_gang.name} Hierarchy:")
for role, members in red_gang.get_hierarchy().items():
    print(f"{role}: {[member.name for member in members]}")
    
# Spawn a Corporation and its members
hannival_corp = Corporation(name="Hannival Corporation")

# Create members
ceo = CEO(name="Mr. Hannival", faction="Hannival Corporation")
manager_1 = Manager(name="Manager Alice", faction="Hannival Corporation")
employee_1 = Employee(name="Employee Bob", faction="Hannival Corporation")
employee_2 = Employee(name="Employee Eve", faction="Hannival Corporation")

# Add members to the corporation
hannival_corp.add_member(ceo)
hannival_corp.add_member(manager_1)
hannival_corp.add_member(employee_1)
hannival_corp.add_member(employee_2)

# CEO sets a faction goal
hannival_corp.set_goal("maximise_profits")
hannival_corp.display_goal()

# Manager adds and delegates tasks
manager_1.add_task("Research new products") # Add the task before delegation
manager_1.add_task("Prepare sales report")
manager_1.delegate_task("Research new products", [employee_1, employee_2])
manager_1.delegate_task("Prepare sales report", [employee_1])

# Attempt to delegate a non-existent task
manager_1.delegate_task("Recruit new employees", [employee_1])

# Print Hannival Corporation hierarchy
print(f"{hannival_corp.name} Hierarchy:")
for role, members in hannival_corp.get_hierarchy().items():
    print(f"{role}: {[member.name for member in members]}")
