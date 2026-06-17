# create_TheState_characters.py

import random
from characters import VIP, Manager, RiotCop, Detective, Taxman, Civilian
from create.create_character_names import create_name
from location.locations import MunicipalBuilding, PoliceStation
from create.create_game_state import get_game_state
from motivation.motivation import MotivationManager
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
from world.scenarios.economy.setup_normal_economy import register_employee

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
    for i, building in enumerate(municipal_buildings):
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
            
            status=status,
            intelligence=15,
                )
        faction.state_staff.append(vip)
        faction.members.append(vip)
        game_state.all_VIPs.append(vip)
        game_state.add_state_staff(vip)
        state_staff.append(vip)
        faction.region.characters_there.append(vip)
        vip.mind = Mind(owner=vip, capacity=vip.intelligence)


        passed_motivations = [
            ("gain_status", 3),
            ("have_fun", 3),
            ("influence", 3),
            ("virtue_signal", 1)
        ]
        initialize_motivations(vip, passed_motivations)
        
        augment_character(vip)
        vip.curiosity = Curiosity(base_score=vip.intelligence // 2)
        vip.task_manager = TaskManager(vip)
        vip.employment = EmployeeProfile()

        #initialize_motivations(vip, vip.motivations)
        #deprecated

        vip.inventory_component = InventoryComponent(vip)
        vip.observation_component = ObservationComponent(owner=vip)
        family_name = vip.family_name
        if family_name not in game_state.extant_family_names:
            game_state.extant_family_names.append(family_name)

    # --- Managers, Employees, Taxmen ---
    for cls, count, status_label, status_level, starting_motivations in [
        (Manager, random.randint(2, 3), "Manager", StatusLevel.MID, [#is a status_label required here?
                ("earn_money", 5),
                ("gain_mid", 4),
                ("virtue_signal", 2),
            ]),

        (Civilian, random.randint(2, 3), "Employee", StatusLevel.MID, [
                ("earn_money", 4),
                ("gain_mid", 4),
            ]),

        (Taxman, random.randint(2, 4), "Taxman", StatusLevel.HIGH, [
                ("earn_money", 3),
                ("virtue_signal", 2),
                ("influence", 2),
                ("find_safety", 3),
            ])
    ]:

        for _ in range(count):
            #set race here
            from config import STATE_RACE
            race = STATE_RACE
            sex = random.choice(["male", "female"])
            building = game_state.municipal_buildings.get(
                faction.region.name
            )
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
                
                status=status
            )
            faction.state_staff.append(person)
            game_state.add_state_staff(person)

            state_staff.append(person)
            faction.members.append(person)
            faction.region.characters_there.append(person)
            person.mind = Mind(owner=person, capacity=person.intelligence)
            augment_character(person)
            person.curiosity = Curiosity(base_score=person.intelligence // 2)
            person.task_manager = TaskManager(person)
            person.employment = EmployeeProfile()
            register_employee(person)
            
            
            initialize_motivations(person, passed_motivations=starting_motivations)

            person.inventory_component = InventoryComponent(character=person)
            person.observation_component = ObservationComponent(owner=person)
            family_name = person.family_name
            if family_name not in game_state.extant_family_names:
                game_state.extant_family_names.append(family_name)

    # --- Police Station ---
    police_stations = [loc for loc in faction.region.locations if isinstance(loc, PoliceStation)]
    copshop = police_stations[0] if police_stations else faction.region.locations[0]

    # --- Riot Cops & Detectives ---
    for cls, count, status_label, status_level, starting_motivations in [
        (
            RiotCop,
            random.randint(2,3),
            "RiotCop",
            StatusLevel.LOW,
            [
                ("patrol", 4),
                ("gain_mid", 4),
                ("virtue_signal", 2),
                ("find_safety", 3),
            ]
        ),

        (
            Detective,
            random.randint(1,2),
            "Detective",
            StatusLevel.MID,
            [
                ("patrol", 4),
                ("investigate_crime", 5),
                ("decrease_hostilities", 3),
                ("snitch", 2),
                ("find_safety", 4),
            ]
        ),

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
                status=status
            )
            initialize_motivations(cop, passed_motivations=starting_motivations)

            faction.state_staff.append(cop)
            game_state.add_state_staff(cop)
            state_staff.append(cop)
            faction.region.characters_there.append(cop)
            cop.mind = Mind(owner=cop, capacity=cop.intelligence)
            augment_character(cop)
            cop.curiosity = Curiosity(base_score=cop.intelligence // 2)
            cop.task_manager = TaskManager(cop)
            cop.employment = EmployeeProfile()
            cop.observation_component = ObservationComponent(owner=cop)

            cop.inventory_component = InventoryComponent(cop)
            family_name = cop.family_name
            if family_name not in game_state.extant_family_names:
                game_state.extant_family_names.append(family_name)

    characters.extend(state_staff)
    #print(f"✅ Created {len(state_staff)} state characters for {faction.name}")
    return characters

