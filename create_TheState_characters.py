# create_TheState_characters.py

import random
from characters import VIP, Manager, Employee, RiotCop, Detective, Taxman
from create_character_names import create_name
from location import MunicipalBuilding, PoliceStation
from create_game_state import get_game_state
from motivation_presets import MotivationPresets
from status import StatusLevel, CharacterStatus, FactionStatus
from base_classes import Character

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

    #muni_building = municipal_buildings[0] if municipal_buildings else faction.region.locations[0]
    #deprecated?

    # --- Create 5 VIPs (1 per region) ---
    for i in range(5):
        building = municipal_buildings[i] if i < len(municipal_buildings) else faction.region.locations[0]
        #todo: check where the VIP characters actually start the game

        # Create and set status for VIP
        status = CharacterStatus()
        status.set_status("public", FactionStatus(StatusLevel.HIGH, "VIP"))
        race, sex, name = generate_identity()
        vip = VIP(
            name=name,
            race=race,
            sex=sex,
            faction=faction,
            region=faction.region,
            location=building,
            initial_motivations=MotivationPresets.for_class("vip"),
            status=status
                )
        faction.state_staff.append(vip)
        game_state.add_state_staff(vip)
        state_staff.append(vip)

    # --- Managers, Employees, Taxmen ---
    for cls, count, motivations, status_label, status_level in [
        (Manager, random.randint(2, 3), MotivationPresets.for_class("Manager"), "Manager", StatusLevel.MID),
        (Employee, random.randint(2, 3), MotivationPresets.for_class("Employee"), "Employee", StatusLevel.MID),
        (Taxman, random.randint(2, 4), MotivationPresets.for_class("Taxman"), "Taxman", StatusLevel.HIGH)
    ]:
        for _ in range(count):
            race, sex, name = generate_identity()
            status = CharacterStatus()
            status.set_status("public", FactionStatus(status_level, status_label))

            person = cls(
                name=name,
                race=race,
                sex=sex,
                faction=faction,
                region=faction.region,
                location=building,
                initial_motivations=motivations,
                status=status
            )
            faction.state_staff.append(person)
            game_state.add_state_staff(person)

            state_staff.append(person)
            faction.members.append(person)
            #Wen adding new state characters, always append to both state_staff and faction.members

    # --- Police Station ---
    police_stations = [loc for loc in faction.region.locations if isinstance(loc, PoliceStation)]
    copshop = police_stations[0] if police_stations else faction.region.locations[0]

    # --- Riot Cops & Detectives ---
    for cls, count, motivations, status_label, status_level in [
        (RiotCop, random.randint(3, 5), MotivationPresets.for_class("RiotCop"), "RiotCop", StatusLevel.LOW),
        (Detective, random.randint(1, 3), MotivationPresets.for_class("Detective"), "Detective", StatusLevel.MID)
    ]:
        for _ in range(count):
            race, sex, name = generate_identity()
            status = CharacterStatus()
            status.set_status("state", FactionStatus(status_level, status_label))

            cop = cls(
                name=name,
                race=race,
                sex=sex,
                faction=faction,
                region=faction.region,
                location=copshop,
                initial_motivations=motivations,
                status=status
            )
            faction.state_staff.append(cop)
            game_state.add_state_staff(cop)
            state_staff.append(cop)

    characters.extend(state_staff)
    #print(f"✅ Created {len(state_staff)} state characters for {faction.name}")
    return characters

def generate_identity(race=None, sex=None):
    """Generate a consistent identity: race, sex, and name based on both."""
    race = race or random.choice(Character.VALID_RACES)
    sex = sex or random.choice(Character.VALID_SEXES)
    name = create_name(race, sex)
    return race, sex, name
#eventually pu this in a utility file and use it in creation files for gang and corp characters etc