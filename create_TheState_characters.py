# create_TheState_characters.py

import random
from characters import VIP, Manager, Employee, RiotCop, Detective, Taxman
from create_character_names import create_name
from location import MunicipalBuilding, PoliceStation
from create_game_state import get_game_state
from motivation_presets import MotivationPresets

def create_TheState_characters(faction):
    from faction import State

    if not isinstance(faction, State) or faction.type != "state":
        raise ValueError(f"Provided faction {faction.name} is not a valid State object.")

    if not faction.region or not faction.region.locations:
        raise ValueError(f"Faction {faction.name} has no valid region or locations.")

    game_state = get_game_state()
    state_staff = []
    characters = []

    # --- Get main building: MunicipalBuilding ---
    municipal_buildings = [loc for loc in faction.region.locations if isinstance(loc, MunicipalBuilding)]
    muni_building = municipal_buildings[0] if municipal_buildings else faction.region.locations[0]

    # --- Create VIP (representing elite leadership) ---
    vip = VIP(
        name=create_name(random.choice(["Terran", "Martian", "German", "French"]), random.choice(["Male", "Female"])),
        faction=faction,
        region=faction.region,
        location=muni_building,
        initial_motivations=MotivationPresets.for_class("vip")
    )
    faction.state_staff.append(vip)
    game_state.add_state_staff(vip)
    state_staff.append(vip)

    # --- Managers, Employees, Taxmen ---
    for cls, count, motivations in [
        (Manager, random.randint(2, 3), MotivationPresets.for_class("Manager")),
        (Employee, random.randint(2, 3), MotivationPresets.for_class("Employee")),
        (Taxman, random.randint(2, 4), MotivationPresets.for_class("Taxman"))
    ]:
        for _ in range(count):
            person = cls(
                name=create_name(random.choice(["Terran", "Martian", "German", "French"]), random.choice(["Male", "Female"])),
                faction=faction,
                region=faction.region,
                location=muni_building,
                initial_motivations=motivations
            )
            faction.state_staff.append(person)
            game_state.add_state_staff(person)
            state_staff.append(person)

    # --- Police Station ---
    police_stations = [loc for loc in faction.region.locations if isinstance(loc, PoliceStation)]
    copshop = police_stations[0] if police_stations else faction.region.locations[0]

    # --- Riot Cops & Detectives ---
    for cls, count, motivations in [
        (RiotCop, random.randint(3, 5), MotivationPresets.for_class("RiotCop")),
        (Detective, random.randint(1, 3), MotivationPresets.for_class("Detective"))
    ]:
        for _ in range(count):
            cop = cls(
                name=create_name(random.choice(["Terran", "Martian", "German", "French"]), random.choice(["Male", "Female"])),
                faction=faction,
                region=faction.region,
                location=copshop,
                initial_motivations=motivations
            )
            faction.state_staff.append(cop)
            game_state.add_state_staff(cop)
            state_staff.append(cop)

    characters.extend(state_staff)
    #print(f"✅ Created {len(state_staff)} state characters for {faction.name}")
    return characters
