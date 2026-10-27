# world.setup_backstory.py

from create.create_game_state import get_game_state
from faction import Gang
import random
from create.create_game_state import get_game_state
from characters import Boss
from character_mind import Mind
from character_components.inventory_component import InventoryComponent
from character_components.observation_component import ObservationComponent
from create.create_character_names import create_name

from create.gang_name_data import RACE_NAME_LOOKUP

from characters import Boss
from character_mind import Mind
from character_components.inventory_component import InventoryComponent
from character_components.observation_component import ObservationComponent
from create.create_character_names import create_name
from create.create_game_state import get_game_state
from faction import Gang
import random


def setup_dead_gang():
    gs = get_game_state()

    # Choose the race of the historical rival gang.
    race = random.choice(Boss.VALID_RACES)

    # Generate a gang name using the same naming scheme as normal gangs.
    # Use the existing RACE_NAME_LOOKUP.
    race_specific_names = RACE_NAME_LOOKUP.get(
        race,
        (["Default"], ["Gang"])
    )

    first_part, second_part = race_specific_names

    while True:
        gang_name = (
            f"{random.choice(first_part)} "
            f"{random.choice(second_part)}"
        )

        if not any(
            gang.name == gang_name
            for gang in gs.gangs
        ):
            break

    rival_gang = Gang(
        name=gang_name,
        violence_disposition=5,
        race=race
    )

    # Create the historical gang Boss.
    sex = random.choice(Boss.VALID_SEXES)

    first_name, family_name, full_name = create_name(
        race,
        sex
    )

    rival_boss = Boss(
        name=full_name,
        first_name=first_name,
        family_name=family_name,
        race=race,
        sex=sex,
        region=None,
        location=None,
        faction=rival_gang
    )

    # Establish the gang ↔ Boss relationship.
    rival_gang.add_boss(rival_boss)

    # This gang and its Boss belong to the backstory.
    rival_gang.defunct = True
    rival_boss.alive = False

    # Give the historical Boss the basic components needed
    # by the cognition/perception systems.
    rival_boss.mind = Mind(
        owner=rival_boss,
        capacity=rival_boss.intelligence
    )

    rival_boss.inventory_component = InventoryComponent(
        rival_boss
    )

    rival_boss.observation_component = ObservationComponent(
        owner=rival_boss
    )

    return rival_gang