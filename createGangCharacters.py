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

def create_gang_characters(faction):

    if faction.type != "gang":
        raise ValueError(f"Faction {faction.name} is not a gang.")

    characters = []

    
    #print(f"Creating Boss for {faction.name}...")

    status = CharacterStatus()
    status.set_status("criminal", FactionStatus(StatusLevel.HIGH, "Boss"))

    sex = random.choice(Character.VALID_SEXES)
    name = create_name(faction.race, sex)
    race = faction.race  # Use race assigned during faction creation

    boss = Boss(
        name=name,
        race=faction.race,#we already set this above?
        sex=sex,
        faction=faction,
        region=faction.region,
        location=None,
        initial_motivations=["gain_high"],
        status=status
    )
    faction.boss = boss  # <-- Store boss reference in gang
    characters.append(boss)
    if faction.HQ:
        faction.boss.location = faction.HQ
        faction.boss.region = faction.HQ.region
    else:
        faction.boss.location = None
        faction.boss.region = faction.region  # fallback, still in region

    # Assign boss to the correct gang in GameState PAUSED/FAILS
    from create_game_state import get_game_state
    game_state = get_game_state()
    for gang in game_state.gangs:
        if gang.name == faction.name:
            gang.add_boss(boss)
            break

    # Captains
    for _ in range(random.randint(2, 3)):
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
            initial_motivations=["gain_high"],
            status=status
        )
        characters.append(captain)
        faction.captains.append(captain)
        faction.members.append(captain)

    # Gang Members
    for _ in range(random.randint(5, 10)):
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
        initial_motivations=["idle"],
        inventory=Inventory([Knife(owner_name=name)]),
        status=status
    )
    characters.append(member)
    
    for char in characters:
        if hasattr(char, "memory"):
            char.memory.add_entry(MemoryEntry(
                subject="weapons_location",
                details="Shops usually have weapons",
                importance=6,
                tags=["weapon", "shop"]
            ), type="semantic")  # Explicitly marking this as a semantic memory
    if char.race != faction.race:
        print(f"[WARNING] {char.name} has race {char.race} but gang {faction.name} is {faction.race}")

    # Gang HQ and Boss Diagnostics
    """ msg = f"Boss {boss.name} created for faction '{faction.name}'"
    assigned = False
    hq_present = False
    located_correctly = False

    from create_game_state import get_game_state
    game_state = get_game_state()

    for gang in game_state.gangs:
        if gang.name == faction.name:
            assigned = gang.boss == boss
            hq_present = gang.HQ is not None
            located_correctly = boss.location == gang.HQ if gang.HQ else False

            if gang.HQ and boss.location is None:
                boss.location = gang.HQ
                boss.region = gang.HQ.region

            msg = f"Boss {boss.name} created for faction '{faction.name}'"
            msg += f"; Assigned to game_state.gang: {'Yes' if assigned else 'No'}"

            if hq_present:
                msg += f"; Gang HQ exists: Yes; Boss located in HQ: {'Yes' if located_correctly else 'No'}"
            else:
                if gang.is_street_gang:
                    msg += "; Gang HQ exists: No, they are a street gang, looking for an HQ."
                else:
                    msg += "; Gang HQ exists: No."
            print(msg)
            break """


    """ # TODO: Add optional gender split logic
    # TODO: Add Gang Assassins if needed later
    # TODO: Log each type created (e.g., # of captains, members) """
    return characters
