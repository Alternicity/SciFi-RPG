# create_TheState_characters.py

import random
from characters import VIP, Manager, Employee, RiotCop, Detective, Taxman
from create.create_character_names import create_name
from location.locations import MunicipalBuilding, PoliceStation
from create.create_game_state import get_game_state
from motivation.motivation import MotivationManager, VALID_MOTIVATIONS
from motivation.motivation_presets import MotivationPresets
from motivation.motivation_init import initialize_motivations
from status import StatusLevel, CharacterStatus, FactionStatus
from base.character import Character
from character_components.inventory_component import InventoryComponent
from character_mind import Mind, Curiosity
from tasks.tasks import TaskManager
from employment.employee import EmployeeProfile
from character_components.observation_component import ObservationComponent
from augment.augment_character import augment_character

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
    for i in range(0):
        building = municipal_buildings[i] if i < len(municipal_buildings) else faction.region.locations[0]
        #todo: check where the VIP characters actually start the game

        # Create and set things for VIP
        race = faction.race#desgin choice - what is the States race, ie, 100% Terran? Hard code that here?
        sex = random.choice(Character.VALID_SEXES)
        #assert race == faction.race, f"Race mismatch when creating State characters: {race} vs {faction.race}"

        first_name, family_name, full_name = create_name(race, sex)
        status = CharacterStatus()
        status.set_status("public", FactionStatus(StatusLevel.HIGH, "VIP"))
        
        vip = VIP(
            name=full_name,
            first_name=first_name,
            family_name=family_name,
            race=race,
            sex=sex,
            faction=faction,
            region=faction.region,
            location=building,
            motivations=[("idle", 1)],
            status=status,
            intelligence=15,
                )
        faction.state_staff.append(vip)
        game_state.add_state_staff(vip)
        state_staff.append(vip)
        vip.mind = Mind(owner=vip, capacity=vip.intelligence)
        augment_character(vip)
        vip.curiosity = Curiosity(base_score=vip.intelligence // 2)
        vip.task_manager = TaskManager(vip)
        vip.employment = EmployeeProfile()
        initialize_motivations(vip, vip.motivations)
        vip.inventory_component = InventoryComponent(owner=vip)
        vip.observation_component = ObservationComponent(owner=vip)
        family_name = vip.family_name
        if family_name not in game_state.extant_family_names:
            game_state.extant_family_names.append(family_name)

    # --- Managers, Employees, Taxmen ---
    for cls, count, motivations, status_label, status_level in [
        (Manager, random.randint(0, 0), MotivationPresets.for_class("Manager"), "Manager", StatusLevel.MID),#2,3
        (Employee, random.randint(0, 0), MotivationPresets.for_class("Employee"), "Employee", StatusLevel.MID),#2, 3
        (Taxman, random.randint(0, 0), MotivationPresets.for_class("Taxman"), "Taxman", StatusLevel.HIGH)#2,4
    ]:
        for _ in range(count):
            #race here is still faction.race
            first_name, family_name, full_name = create_name(race, sex)
            status = CharacterStatus()
            status.set_status("public", FactionStatus(status_level, status_label))

            person = cls(
                name=full_name,
                first_name=first_name,
                family_name=family_name,
                race=race,
                sex=sex,
                faction=faction,
                region=faction.region,
                location=building,
                motivations=[("idle", 1)],
                status=status
            )
            faction.state_staff.append(person)
            game_state.add_state_staff(person)

            state_staff.append(person)
            faction.members.append(person)

            person.mind = Mind(owner=person, capacity=person.intelligence)
            augment_character(person)
            person.curiosity = Curiosity(base_score=person.intelligence // 2)
            person.task_manager = TaskManager(person)
            person.employment = EmployeeProfile()
            initialize_motivations(person, person.motivations)
            person.inventory_component = InventoryComponent(owner=person)
            person.observation_component = ObservationComponent(owner=person)
            family_name = person.family_name
            if family_name not in game_state.extant_family_names:
                game_state.extant_family_names.append(family_name)

    # --- Police Station ---
    police_stations = [loc for loc in faction.region.locations if isinstance(loc, PoliceStation)]
    copshop = police_stations[0] if police_stations else faction.region.locations[0]

    # --- Riot Cops & Detectives ---
    for cls, count, motivations, status_label, status_level in [
        (RiotCop, random.randint(0, 0), MotivationPresets.for_class("RiotCop"), "RiotCop", StatusLevel.LOW),#3,5
        (Detective, random.randint(0, 0), MotivationPresets.for_class("Detective"), "Detective", StatusLevel.MID)#2, 3
    ]:
        for _ in range(count):
            #race here is still faction.race
            first_name, family_name, full_name = create_name(race, sex)

            status = CharacterStatus()
            status.set_status("state", FactionStatus(status_level, status_label))

            cop = cls(
                name=full_name,
                first_name=first_name,
                family_name=family_name,
                race=race,
                sex=sex,
                faction=faction,
                region=faction.region,
                location=copshop,
                motivations=[("idle", 1)],
                status=status
            )
            faction.state_staff.append(cop)
            game_state.add_state_staff(cop)
            state_staff.append(cop)
            cop.mind = Mind(owner=cop, capacity=cop.intelligence)
            augment_character(cop)
            cop.curiosity = Curiosity(base_score=cop.intelligence // 2)
            cop.task_manager = TaskManager(cop)
            cop.employment = EmployeeProfile()
            initialize_motivations(cop, cop.motivations)
            cop.inventory_component = InventoryComponent(owner=cop)
            family_name = cop.family_name
            if family_name not in game_state.extant_family_names:
                game_state.extant_family_names.append(family_name)

    characters.extend(state_staff)
    #print(f"✅ Created {len(state_staff)} state characters for {faction.name}")
    return characters

