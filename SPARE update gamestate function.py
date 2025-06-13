#Add this logic inside your loop in create.py:

region_name = assigned_region.name.lower().replace(" ", "") #long version

# Create a map from region names to GameState attributes
region_gang_lists = {
    "downtown": game_state.downtown_gangs,
    "northville": game_state.northville_gangs,
    "easternhole": game_state.easternhole_gangs,
    "westborough": game_state.westborough_gangs,
    "southville": game_state.southville_gangs,
}

# Append to the right list
if region_name in region_gang_lists:
    region_gang_lists[region_name].append(gang)
else:
    print(f"[Warning] Unknown region '{assigned_region.name}' for gang '{gang.name}'")