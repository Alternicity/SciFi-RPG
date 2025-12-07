#createCorporations, code cut from previous bloated file
#do not import this file: character_creation_funcs.py
import random
from characters import CEO, Manager, CorporateSecurity, CorporateAssasin, Employee, Accountant
from location.locations import HQ
from create.create_character_names import create_name
from motivation.motivation import MotivationManager, VALID_MOTIVATIONS
from motivation.motivation_presets import MotivationPresets
from motivation.motivation_init import initialize_motivations
from status import CharacterStatus, FactionStatus, StatusLevel
from base.character import Character
from character_components.inventory_component import InventoryComponent
from character_mind import Mind, Curiosity
from tasks.tasks import TaskManager
from employment.employee import EmployeeProfile
from character_components.observation_component import ObservationComponent
from create.create_game_state import get_game_state
game_state = get_game_state()

def create_corporation_characters(faction, factions):
    """
    Creates characters for a corporate faction.

    :param faction: The faction for which characters are being created.
    :param factions: A list of all factions, needed to identify corporations.
    :return: A list of character instances for this faction.
    The function only creates characters for the passed-in faction, even though 
    the factions list is available—it is not iterating over all corporations, just 
    validating or checking against the list if needed.
    If in the future you want to iterate through all corporations, that should 
    happen in the orchestration function like create_all_characters() — not here
    """

    if faction.type != "corporation":
        raise ValueError(f"Faction {faction.name} is not a corporation.")
    if factions is None:
        raise ValueError("Factions list is required for corporation character generation.")

    from faction import Corporation #not accessed
    characters = []

    # Locate HQ belonging to this faction
    corp_hqs = [
        loc for loc in faction.region.locations
        if isinstance(loc, HQ) and loc.faction == faction
    ]
    corp_hq = corp_hqs[0] if corp_hqs else None

    # Create CEO
    status = CharacterStatus()
    status.set_status("public", FactionStatus(StatusLevel.HIGH, "CEO"))
    
    race = random.choice(Character.VALID_RACES)
    sex = random.choice(Character.VALID_SEXES)
    first_name, family_name, full_name = create_name(race, sex)

    ceo = CEO(
        name=full_name,
        first_name=first_name,
        family_name=family_name,
        race=race,
        sex=sex,
        faction=faction,
        region=faction.region,
        location=corp_hq,
        motivations=[("idle", 1)],
        status=status
    )
    faction.add_CEO(ceo)
    characters.append(ceo)

    ceo.mind = Mind(owner=ceo, capacity=ceo.intelligence)
    ceo.curiosity = Curiosity(base_score=ceo.intelligence // 2)
    ceo.task_manager = TaskManager(ceo)
    ceo.employment = EmployeeProfile()
    initialize_motivations(ceo, ceo.motivations)
    ceo.inventory_component = InventoryComponent(owner=ceo)
    ceo.observation_component = ObservationComponent(owner=ceo)
    family_name = ceo.family_name
    if family_name not in game_state.extant_family_names:
        game_state.extant_family_names.append(family_name)

    # Managers
    for _ in range(random.randint(2, 3)):
        status = CharacterStatus()
        status.set_status("public", FactionStatus(StatusLevel.MID, "Manager"))
        race = random.choice(Character.VALID_RACES)
        sex = random.choice(Character.VALID_SEXES)
        first_name, family_name, full_name = create_name(race, sex)

        manager = Manager(
            name=full_name,
            first_name=first_name,
            family_name=family_name,
            race=race,
            sex=sex,
            faction=faction,
            region=faction.region,
            location=corp_hq,
            motivations=[("idle", 1)],
            status=status
        )
        faction.add_manager(manager)
        characters.append(manager)
        manager.mind = Mind(owner=manager, capacity=manager.intelligence)
        manager.curiosity = Curiosity(base_score=manager.intelligence // 2)
        manager.task_manager = TaskManager(manager)
        manager.employment = EmployeeProfile()
        initialize_motivations(manager, manager.motivations)
        manager.inventory_component = InventoryComponent(owner=manager)
        manager.observation_component = ObservationComponent(owner=manager)
        family_name = manager.family_name
        if family_name not in game_state.extant_family_names:
            game_state.extant_family_names.append(family_name)

    # Employees
    for _ in range(random.randint(3, 6)):
        status = CharacterStatus()
        status.set_status("public", FactionStatus(StatusLevel.LOW, "Employee"))
        race = random.choice(Character.VALID_RACES)
        sex = random.choice(Character.VALID_SEXES)
        first_name, family_name, full_name = create_name(race, sex)

        employee = Employee(
            name=full_name,
            first_name=first_name,
            family_name=family_name,
            race=race,
            sex=sex,
            faction=faction,
            region=faction.region,
            location=corp_hq,
            motivations=[("idle", 1)],
            status=status
        )
        faction.add_employee(employee)
        characters.append(employee)
        employee.mind = Mind(owner=employee, capacity=employee.intelligence)
        employee.curiosity = Curiosity(base_score=employee.intelligence // 2)
        employee.task_manager = TaskManager(employee)
        employee.employment = EmployeeProfile()
        initialize_motivations(employee, employee.motivations)
        employee.inventory_component = InventoryComponent(owner=employee)
        employee.observation_component = ObservationComponent(owner=employee)
        family_name = employee.family_name
        if family_name not in game_state.extant_family_names:
            game_state.extant_family_names.append(family_name)

    # Security
    for _ in range(random.randint(2, 4)):
        status = CharacterStatus()
        status.set_status("public", FactionStatus(StatusLevel.MID, "Guard"))
        race = random.choice(Character.VALID_RACES)
        sex = random.choice(Character.VALID_SEXES)
        first_name, family_name, full_name = create_name(race, sex)

        guard = CorporateSecurity(
            name=full_name,
            first_name=first_name,
            family_name=family_name,
            race=race,
            sex=sex,
            faction=faction,
            region=faction.region,
            location=corp_hq,
            motivations=[("idle", 1)],
            status=status
        )
        faction.add_security(guard)
        characters.append(guard)
        guard.mind = Mind(owner=guard, capacity=guard.intelligence)
        guard.curiosity = Curiosity(base_score=guard.intelligence // 2)
        guard.task_manager = TaskManager(guard)
        guard.employment = EmployeeProfile()
        initialize_motivations(guard, guard.motivations)
        guard.inventory_component = InventoryComponent(owner=guard)
        guard.observation_component = ObservationComponent(owner=guard)
        family_name = guard.family_name
        if family_name not in game_state.extant_family_names:
            game_state.extant_family_names.append(family_name)


    # Accountants
    for _ in range(random.randint(1, 3)):
        status = CharacterStatus()
        status.set_status("public", FactionStatus(StatusLevel.MID, "Accountant"))
        race = random.choice(Character.VALID_RACES)
        sex = random.choice(Character.VALID_SEXES)
        first_name, family_name, full_name = create_name(race, sex)

        accountant = Accountant(
            name=full_name,
            first_name=first_name,
            family_name=family_name,
            race=race,
            sex=sex,
            faction=faction,
            region=faction.region,
            location=corp_hq,
            motivations=[("idle", 1)],
            status=status
        )
        faction.add_accountant(accountant)
        characters.append(accountant)
        accountant.mind = Mind(owner=accountant, capacity=accountant.intelligence)
        accountant.curiosity = Curiosity(base_score=accountant.intelligence // 2)
        accountant.task_manager = TaskManager(accountant)
        accountant.employment = EmployeeProfile()
        initialize_motivations(accountant, accountant.motivations)
        accountant.inventory_component = InventoryComponent(owner=accountant)
        accountant.observation_component = ObservationComponent(owner=accountant)
        family_name = accountant.family_name
        if family_name not in game_state.extant_family_names:
            game_state.extant_family_names.append(family_name)

    # Corporate Assassins
    for _ in range(random.randint(0, 2)):
        status = CharacterStatus()
        status.set_status("public", FactionStatus(StatusLevel.MID, "Unclear"))
        race = random.choice(Character.VALID_RACES)
        sex = random.choice(Character.VALID_SEXES)
        first_name, family_name, full_name = create_name(race, sex)

        assassin = CorporateAssasin(
            name=full_name,
            first_name=first_name,
            family_name=family_name,
            race=race,
            sex=sex,
            faction=faction,
            region=faction.region,
            location=corp_hq,
            motivations=[("idle", 1)],
            status=status
        )
        characters.append(assassin)
        assassin.mind = Mind(owner=assassin, capacity=assassin.intelligence)
        assassin.curiosity = Curiosity(base_score=assassin.intelligence // 2)
        assassin.task_manager = TaskManager(assassin)
        assassin.employment = EmployeeProfile()
        initialize_motivations(assassin, assassin.motivations)
        assassin.inventory_component = InventoryComponent(owner=assassin)
        assassin.observation_component = ObservationComponent(owner=assassin)
        family_name = assassin.family_name
        if family_name not in game_state.extant_family_names:
            game_state.extant_family_names.append(family_name)
    return characters