#createCorporations, code cut from previous bloated file
#do not import this file: character_creation_funcs.py
import random
from characters import CEO, Manager, CorporateSecurity, CorporateAssasin, Employee, Accountant
from location import HQ
from create_character_names import create_name
from motivation_presets import MotivationPresets
from status import CharacterStatus, FactionStatus, StatusLevel
from base_classes import Character

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

    from faction import Corporation
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
    name = create_name(race, sex)

    ceo = CEO(
        name=name,
        race=race,
        sex=sex,
        faction=faction,
        region=faction.region,
        location=corp_hq,
        initial_motivations=MotivationPresets.for_class("CEO"),
        status=status
    )
    faction.add_CEO(ceo)
    characters.append(ceo)

    # Managers
    for _ in range(random.randint(2, 3)):
        status = CharacterStatus()
        status.set_status("public", FactionStatus(StatusLevel.MID, "Manager"))
        race = random.choice(Character.VALID_RACES)
        sex = random.choice(Character.VALID_SEXES)
        name = create_name(race, sex)

        manager = Manager(
            name=name,
            race=race,
            sex=sex,
            faction=faction,
            region=faction.region,
            location=corp_hq,
            initial_motivations=MotivationPresets.for_class("Manager"),
            status=status
        )
        faction.add_manager(manager)
        characters.append(manager)

    # Employees
    for _ in range(random.randint(3, 6)):
        status = CharacterStatus()
        status.set_status("public", FactionStatus(StatusLevel.LOW, "Employee"))
        race = random.choice(Character.VALID_RACES)
        sex = random.choice(Character.VALID_SEXES)
        name = create_name(race, sex)

        employee = Employee(
            name=name,
            race=race,
            sex=sex,
            faction=faction,
            region=faction.region,
            location=corp_hq,
            initial_motivations=MotivationPresets.for_class("Employee"),
            status=status
        )
        faction.add_employee(employee)
        characters.append(employee)

    # Security
    for _ in range(random.randint(2, 4)):
        status = CharacterStatus()
        status.set_status("public", FactionStatus(StatusLevel.MID, "Guard"))
        race = random.choice(Character.VALID_RACES)
        sex = random.choice(Character.VALID_SEXES)
        name = create_name(race, sex)

        guard = CorporateSecurity(
            name=name,
            race=race,
            sex=sex,
            faction=faction,
            region=faction.region,
            location=corp_hq,
            initial_motivations=MotivationPresets.for_class("CorporateSecurity"),
            status=status
        )
        faction.add_security(guard)
        characters.append(guard)

    # Accountants
    for _ in range(random.randint(1, 3)):
        status = CharacterStatus()
        status.set_status("public", FactionStatus(StatusLevel.MID, "Accountant"))
        race = random.choice(Character.VALID_RACES)
        sex = random.choice(Character.VALID_SEXES)
        name = create_name(race, sex)

        accountant = Accountant(
            name=name,
            race=race,
            sex=sex,
            faction=faction,
            region=faction.region,
            location=corp_hq,
            initial_motivations=MotivationPresets.for_class("Accountant"),
            status=status
        )
        faction.add_accountant(accountant)
        characters.append(accountant)

    # Corporate Assassins
    for _ in range(random.randint(0, 2)):
        status = CharacterStatus()
        status.set_status("public", FactionStatus(StatusLevel.MID, "Unclear"))
        race = random.choice(Character.VALID_RACES)
        sex = random.choice(Character.VALID_SEXES)
        name = create_name(race, sex)

        assassin = CorporateAssasin(
            name=name,
            race=race,
            sex=sex,
            faction=faction,
            region=faction.region,
            location=corp_hq,
            initial_motivations=MotivationPresets.for_class("CorporateAssassin"),
            status=status
        )
        characters.append(assassin)

    return characters