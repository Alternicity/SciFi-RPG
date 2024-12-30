import json

def simulate_day(characters, locations):
    """
    Simulates a day in the game.
    """
    # Day shift
    for char in characters:
        if char.shift == 'day':
            if char.is_working:
                print(f"{char.name} is working at {char.current_location.name}.")
            else:
                char.current_location = find_leisure_location(char, locations)
                print(f"{char.name} is relaxing at {char.current_location.name}.")

    # Update fun and hunger
    for char in characters:
        if char.is_working:
            char.fun -= 1  # Working reduces fun
        else:
            char.fun += 1  # Leisure increases fun
        char.hunger += 1  # Hunger always increases

    # Night shift
    for char in characters:
        if char.shift == 'night':
            if char.is_working:
                print(f"{char.name} is working at {char.current_location.name}.")
            else:
                char.current_location = find_leisure_location(char, locations)
                print(f"{char.name} is relaxing at {char.current_location.name}.")

def save_simulation_data(characters, locations, day):
    data = {
        "day": day,
        "characters": [
            {
                "name": char.name,
                "role": char.role,
                "location": char.current_location.name if char.current_location else None,
                "fun": char.fun,
                "hunger": char.hunger,
                "is_working": char.is_working
            }
            for char in characters
        ],
        "locations": [
            {
                "name": loc.name,
                "type": loc.type,
                "workers": [worker.name for worker in loc.current_workers]
            }
            for loc in locations
        ]
    }
    with open(f"simulation_day_{day}.json", "w") as file:
        json.dump(data, file, indent=4)
