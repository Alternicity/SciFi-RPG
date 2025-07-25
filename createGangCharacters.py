#createGangCharacter.py
import random
from characters import Boss, Captain, GangMember
from create_character_names import create_name
from create_game_state import get_game_state
from motivation_presets import MotivationPresets
from status import StatusLevel, CharacterStatus, FactionStatus
from base_classes import Character
from weapons import Knife
from inventory import Inventory
from character_memory import MemoryEntry
#no ai import here
def create_gang_characters(faction, all_regions):

    if faction.type != "gang":
        raise ValueError(f"Faction {faction.name} is not a gang.")

    characters = []

    if faction.is_street_gang:
        region = faction.region
        region_locations = region.get_all_locations()
        preferred_types = ["Park", "VacantLot", "ApartmentBlock", "PoliceStation"]
        preferred = [loc for loc in region_locations if loc.__class__.__name__ in preferred_types]

        start_location = random.choice(preferred if preferred else region_locations)
        faction.street_gang_start_location = start_location

        # Optional dramatic print
        print(f"[INIT] Members of street gang '{faction.name}' will start at '{start_location.name}' in region '{region.name}'")
    
        # Add to region's street gang list
        if faction not in region.region_street_gangs:
            region.region_street_gangs.append(faction)

    #print(f"Creating Boss for {faction.name}...")

    status = CharacterStatus()
    status.set_status("criminal", FactionStatus(StatusLevel.HIGH, "Boss"))

    sex = random.choice(Character.VALID_SEXES)
    name = create_name(faction.race, sex)
    race = faction.race  
    #uncomment
    """ boss = Boss(
        name=name,
        race=faction.race,
        sex=sex,
        faction=faction,
        region=faction.region,
        location=None,
        motivations=MotivationPresets.for_class("Boss"),
        status=status
    )
    if faction.is_street_gang and faction.street_gang_start_location:
        boss.location = faction.street_gang_start_location
    elif faction.HQ:
        boss.location = faction.HQ
    else:
        print(f"[ERROR] {faction.name} has no HQ and no valid start location.")

    faction.boss = boss  # <-- Store boss reference in gang
    characters.append(boss)
    faction.region.characters_there.append(boss) """
#not neccesary to uncomment to restore gang chars instantiation
    """ if faction.HQ:
        faction.boss.location = faction.HQ #it seems this works for Bosses
        faction.boss.region = faction.HQ.region
    else:
        if faction.is_street_gang and faction.street_gang_start_location:
            faction.boss.location = faction.street_gang_start_location
            faction.boss.region = faction.region
        else:
            print(f"[ERROR] {faction.name} has no HQ and no street_gang_start_location. Boss location is undefined.")
            faction.boss.location = None
            faction.boss.region = faction.region """
#uncomment
    """ from create_game_state import get_game_state
    game_state = get_game_state()
    for gang in game_state.gangs:
        if gang.name == faction.name:
            gang.add_boss(boss)
            break """

    # Captains
    for _ in range(random.randint(0, 0)):#2,3
        status = CharacterStatus()
        status.set_status("criminal", FactionStatus(StatusLevel.MID, "Captain"))
        
        sex = random.choice(Character.VALID_SEXES)
        assert race == faction.race, f"Race mismatch when creating gang characters: {race} vs {faction.race}"
        name = create_name(race, sex)

        captain = Captain(
            name=name,
            race=faction.race,
            sex=sex,
            faction=faction,
            region=faction.region,
            location=None,
            motivations=MotivationPresets.for_class("Captain"),

            status=status
        )
        
        faction.captains.append(captain)
        faction.members.append(captain)

        if faction.is_street_gang and faction.street_gang_start_location:
            captain.location = faction.street_gang_start_location
        elif faction.HQ:
            captain.location = faction.HQ
        characters.append(captain)
        faction.region.characters_there.append(captain)

    # Gang Members
    for _ in range(random.randint(1,1)):#5, 10
        status = CharacterStatus()
        status.set_status("criminal", FactionStatus(StatusLevel.LOW, "Ganger"))
        
        sex = random.choice(Character.VALID_SEXES)
        name = create_name(race, sex)
        
        member = GangMember(
        name=name,
        race=faction.race,
        sex=sex,
        faction=faction,
        region=faction.region,
        location=None,
        origin=faction.region,
        motivations=[("idle", 1)],
        inventory=Inventory([Knife(owner_name=name)]),
        status=status
    )

        faction.members.append(member)
        
        if faction.is_street_gang and faction.street_gang_start_location:
            member.location = faction.street_gang_start_location
        elif faction.HQ:
            member.location = faction.HQ
        characters.append(member)
        faction.region.characters_there.append(member)
    
    for char in characters:
        if hasattr(char, "memory"):
            char.mind.memory.add_entry(MemoryEntry(
                subject="Shop",
                object_="ranged_weapon",
                details="Shops usually have weapons",
                importance=6,
                tags=["weapon", "shop"],
                type=("streetwise"),
                initial_memory_type="episodic",
                function_reference=None,
                implementation_path=None,
                associated_function=None
            ))
            
    if char.race != faction.race:
        print(f"[WARNING] {char.name} has race {char.race} but gang {faction.name} is {faction.race}")

        print_gang_densities(all_regions)

    return characters
    
def print_gang_densities(all_regions):
    already_logged = set()

    for region in all_regions:
        for gang in region.region_street_gangs:
            loc = getattr(gang, "street_gang_start_location", None)
            if loc:
                key = (gang.name, region.name)
                if key not in already_logged:
                    count = sum(1 for c in region.characters_there if getattr(c, "faction", None) == gang)
                    if count > 0:
                        print(f"[DENSITY] {count} members of street gang '{gang.name}' are starting at '{loc}' in region '{region.name}'")
                        already_logged.add(key)

