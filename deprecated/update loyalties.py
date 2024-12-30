def update_loyalties(): #from an older main.py
    for region, data in city_data["regions"].items():
        for faction in data["factions"]:
            # Check faction status and adjust loyalty
            for character in data["characters"]:
                loyalty = character["loyalties"].get(faction, 50)
                # Modify loyalty based on faction status or events
                loyalty += random.randint(-5, 5)  # Example of random fluctuation
                character["loyalties"][faction] = max(0, min(100, loyalty))  # Ensure loyalty stays within bounds