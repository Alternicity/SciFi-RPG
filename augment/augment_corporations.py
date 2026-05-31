#augment.augment_corporations.py
from create.create_game_state import get_game_state
game_state = get_game_state()
import random
from world.scenarios.economy.economy_logging import economy_log
from location.locations import Powerplant, Factory
from faction import Corporation

def augment_corporations():

    print(f"[DEBUG] corporations: {len(game_state.corporations)}")

    gs = get_game_state()

    corporations = [
        f for f in gs.factions
        if isinstance(f, Corporation)
    ]

    factories = [
        loc for loc in gs.all_locations
        if isinstance(loc, Factory)
    ]

    powerplants = [
        loc for loc in gs.all_locations
        if isinstance(loc, Powerplant)
    ]

    random.shuffle(corporations)
    from economy.economy_helpers import assign_location_owner
    """ for corp, plant in zip(corporations, powerplants):

        assign_location_owner(
            plant,
            corp
        )

    for corp, factory in zip(corporations, factories):

        assign_location_owner(
            factory,
            corp
        ) """

    """     print(
            "[AUGMENT CORP]",
            plant.name,
            "->",
            corp.name
        )

        print(
            "[AUGMENT CORP]",
            factory.name,
            "->",
            corp.name
        ) """

def assign_power_workers(corp):
    assigned = set()

    powerplants = [
        loc for loc in corp.owned_locations
        if isinstance(loc, Powerplant)
    ]

    for plant in powerplants:

        for _ in range(2):

            available = [
                w for w in corp.available_workers
                if w not in assigned
            ]

            if not available:
                break

            worker = random.choice(available)

            assigned.add(worker)

            worker.location = plant
            worker.region = plant.region
            from utils import employ_npc
            from employment.roles import LINE_WORKER
            employ_npc(
                worker,
                plant,
                LINE_WORKER,
                shift="day",
                shift_start=1,
                shift_end=8
            )

            if worker not in plant.employees_there:
                plant.employees_there.append(worker)

            if worker not in corp.employees:
                corp.employees.append(worker)

            """ economy_log(
                f"[WORKER] {worker.name} -> {plant.name}"
            ) """

def assign_factory_workers(corp):
    assigned = set()

    factories = [
        loc for loc in corp.owned_locations
        if isinstance(loc, Factory)
    ]

    for plant in factories:

        for _ in range(2):

            available = [
                w for w in corp.available_workers
                if w not in assigned
            ]

            if not available:
                break

            worker = random.choice(available)

            assigned.add(worker)

            worker.location = plant
            worker.region = plant.region
            from utils import employ_npc
            from employment.roles import LINE_WORKER
            employ_npc(
                worker,
                plant,
                LINE_WORKER,
                shift="day",
                shift_start=1,
                shift_end=8
            )

            if worker not in plant.employees_there:
                plant.employees_there.append(worker)
            if worker not in corp.employees:
                corp.employees.append(worker)

            """ economy_log(
                f"[WORKER] {worker.name} -> {plant.name}"
            ) """
    #pick a small number of corporations, assign ownership of powerplants and factories
    