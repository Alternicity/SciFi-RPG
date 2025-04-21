import random
from characters import Boss, Captain, GangMember
from create_character_names import create_name
from create_game_state import get_game_state
from motivation_presets import MotivationPresets

def create_gang_characters(faction):
    """
    Creates characters for a gang faction.

    :param faction: The gang faction to generate characters for.
    :return: A list of character instances for this gang.
    """
    if faction.type != "gang":
        raise ValueError(f"Faction {faction.name} is not a gang.")

    characters = []

    faction_race = faction.race  # Use race assigned during faction creation
    print(f"Creating Boss for {faction.name}...")
    #character names will need to be drawn from the race specific csv files, gangs begin racially homogenous
    boss = Boss(
        name=create_name(faction_race, random.choice(["Male", "Female"])),
        race=faction_race,
        faction=faction,
        region=faction.region,
        location=None,
        initial_motivations=["gain_high"]
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
        captain = Captain(
            name=create_name(faction_race, random.choice(["Male", "Female"])),
            race=faction_race,
            faction=faction,
            region=faction.region,
            location=None,
            initial_motivations=["gain_high"]
        )
        characters.append(captain)
        faction.captains.append(captain)
        faction.members.append(captain)

    # Gang Members
    for _ in range(random.randint(5, 10)):
        member = GangMember(
        name=create_name(faction_race, random.choice(["Male", "Female"])),
        race=faction_race,
        faction=faction,
        region=faction.region,
        location=None,
        initial_motivations=["gain_mid"]
    )
    characters.append(member)
    faction.members.append(member)

    """ # TODO: Add optional gender split logic
    # TODO: Add Gang Assassins if needed later
    # TODO: Log each type created (e.g., # of captains, members) """
    return characters
