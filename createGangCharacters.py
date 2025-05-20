import random
from characters import Boss, Captain, GangMember
from create_character_names import create_name
from create_game_state import get_game_state
from motivation_presets import MotivationPresets
from status import StatusLevel, CharacterStatus, FactionStatus
from base_classes import Character

def create_gang_characters(faction):

    if faction.type != "gang":
        raise ValueError(f"Faction {faction.name} is not a gang.")

    characters = []

    
    print(f"Creating Boss for {faction.name}...")
    #character names will need to be drawn from the race specific csv files, gangs begin racially homogenous
    
    status = CharacterStatus()
    status.set_status("criminal", FactionStatus(StatusLevel.HIGH, "Boss"))

    sex = random.choice(Character.VALID_SEXES)
    name = create_name(race, sex)
    race = faction.race  # Use race assigned during faction creation

    boss = Boss(
        name=name,
        race=race,
        sex=sex,
        faction=faction,
        region=faction.region,
        location=None,
        initial_motivations=["gain_high"],
        status=status
    )
    faction.boss = boss  # <-- Store boss reference in gang
    characters.append(boss)

    # Assign boss to the correct gang in GameState
    game_state = get_game_state()
    for gang in game_state.gangs:
        if gang.name == faction.name:
            gang.add_boss(boss)
            break
    print(f"Boss Created: {boss.name} (Faction: {faction.name})")

    # Captains
    for _ in range(random.randint(2, 3)):
        status = CharacterStatus()
        status.set_status("criminal", FactionStatus(StatusLevel.MID, "Captain"))
        
        sex = random.choice(Character.VALID_SEXES)
        name = create_name(race, sex)

        captain = Captain(
            name=name,
            race=race,
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
        race=race,
        sex=sex,
        faction=faction,
        region=faction.region,
        location=None,
        initial_motivations=["gain_mid"],
        status=status
    )
    characters.append(member)
    faction.members.append(member)

    """ # TODO: Add optional gender split logic
    # TODO: Add Gang Assassins if needed later
    # TODO: Log each type created (e.g., # of captains, members) """
    return characters
