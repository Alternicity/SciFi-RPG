#create.createGangCharacter.py
import random
from characters import Boss, Captain, GangMember
from create.create_character_names import create_name
from create.create_game_state import get_game_state

from motivation.motivation import MotivationManager, VALID_MOTIVATIONS
from motivation.motivation_presets import MotivationPresets
from motivation.motivation_init import initialize_motivations

from status import StatusLevel, CharacterStatus, FactionStatus
from base.character import Character
from weapons import Knife

from character_components.inventory_component import InventoryComponent
from inventory import Inventory
from character_memory import MemoryEntry
from character_components.observation_component import ObservationComponent
from debug_utils import debug_print, add_character
from character_mind import Mind, Curiosity
from tasks.tasks import TaskManager
from employment.employee import EmployeeProfile
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
        debug_print(npc=None, message=f"[INIT] Members of street gang '{faction.name}' will start at '{start_location.name}' in region '{region.name}'", category="create")

        # Add to region's street gang list
        if faction not in region.region_street_gangs:
            region.region_street_gangs.append(faction)#doesnt appear to update gamestate variables

    #print(f"Creating Boss for {faction.name}...")

    status = CharacterStatus()
    status.set_status("criminal", FactionStatus(StatusLevel.HIGH, "Boss"))

    sex = random.choice(Character.VALID_SEXES)
    race = faction.race#double check this
    first_name, family_name, full_name = create_name(race, sex)
    
    #uncomment
    """ boss = Boss(
        name=full_name,
        first_name=first_name,
        family_name=family_name,
        race=faction.race,
        sex=sex,
        faction=faction,
        region=faction.region,
        location=None,
        motivations=[("idle", 1)],
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
    faction.region.characters_there.append(boss)
    boss.mind = Mind(owner=boss, capacity=boss.intelligence)
    boss.curiosity = Curiosity(base_score=boss.intelligence // 2)
    boss.task_manager = TaskManager(boss)
    boss.employment = EmployeeProfile()
    initialize_motivations(boss, member.motivations)
    boss.inventory_component = InventoryComponent(owner=boss)
    boss.observation_component = ObservationComponent(owner=boss)
      """
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
        first_name, family_name, full_name = create_name(race, sex)



        captain = Captain(
            name=full_name,
            first_name=first_name,
            family_name=family_name,
            race=faction.race,
            sex=sex,
            faction=faction,
            region=faction.region,
            location=None,
            motivations=[("idle", 1)],

            status=status
        )
        
        faction.captains.append(captain)
        faction.members.append(captain)
        captain.mind = Mind(owner=captain, capacity=captain.intelligence)
        captain.curiosity = Curiosity(base_score=captain.intelligence // 2)
        captain.task_manager = TaskManager(captain)
        captain.employment = EmployeeProfile()
        initialize_motivations(captain, member.motivations)
        captain.inventory_component = InventoryComponent(owner=captain)
        captain.observation_component = ObservationComponent(owner=captain)
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
        assert race == faction.race, f"Race mismatch when creating gang characters: {race} vs {faction.race}"

        first_name, family_name, full_name = create_name(race, sex)
        
        member = GangMember(
        name=full_name,
        first_name=first_name,
        family_name=family_name,
        race=faction.race,
        sex=sex,
        faction=faction,
        region=faction.region,
        location=None,
        origin=faction.region,
        status=status
    )
        member.inventory_component = InventoryComponent(member)#added as a component
        knife = Knife()
        member.inventory.add_item(knife)#function adds ownership also, so I must check how in light of name changes above

        faction.members.append(member)
        member.mind = Mind(owner=member, capacity=member.intelligence)
        member.curiosity = Curiosity(base_score=member.intelligence // 2)
        member.task_manager = TaskManager(member)
        member.employment = EmployeeProfile()
        
        member.motivation_manager = MotivationManager(member)
        initialize_motivations(member, passed_motivations=[("idle", 1)])
        
        member.observation_component = ObservationComponent(owner=member)

        if faction.is_street_gang and faction.street_gang_start_location:
            member.location = faction.street_gang_start_location
        elif faction.HQ:
            member.location = faction.HQ
            add_character(faction.HQ, member)#I only just added this
        else:
            member.location = None#New. Why? Does this line break street gang random placement?

        # *** Ensure the location object records the member ***
        #Note : does this block just replicate the add_character call above?
        if getattr(member, "location", None):
            loc = member.location
            # defensive: ensure characters_there exists and avoid duplicates
            if not hasattr(loc, "characters_there"):
                loc.characters_there = []
            if member not in loc.characters_there:
                loc.characters_there.append(member)
                # optional debug
                debug_print(member, f"[INIT] Registered {member.name} in {loc.name}.", category="placement")
        else:
            debug_print(member, f"[INIT] {member.name} created with no location (faction={faction.name}).", category="placement")



        characters.append(member)
        faction.region.characters_there.append(member)
    
    for char in characters:
        if hasattr(char, "memory"):
            char.mind.memory.add_entry(MemoryEntry(#should this use add_episodcic or semantic?
                subject="Shop",
                object_="ranged_weapon",
                details="Shops usually have weapons",
                importance=6,
                tags=["weapon", "shop"],
                type=("streetwise"),
                initial_memory_type="semantic",
                function_reference=None,
                implementation_path=None,
                associated_function=None
            ))
            
    if char.race != faction.race:
        debug_print(npc=None, message=f"[WARNING] {char.name} has race {char.race} but gang {faction.name} is {faction.race}", category="create")

        print_gang_densities(all_regions)

    return characters
    
def print_gang_densities(all_regions):#ONLY PRINTS STREET GANGS I THINK
    already_logged = set()

    for region in all_regions:
        for gang in region.region_street_gangs:
            loc = getattr(gang, "street_gang_start_location", None)
            if loc:
                key = (gang.name, region.name)
                if key not in already_logged:
                    count = sum(1 for c in region.characters_there if getattr(c, "faction", None) == gang)
                    if count > 0:
                        debug_print(npc=None, message=f"[DENSITY] {count} members of street gang '{gang.name}' are starting at '{loc}' in region '{region.name}'", category="create")
                        already_logged.add(key)

