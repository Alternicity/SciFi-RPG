#createCorporations, code cut from previous bloated file
#do not import this file: character_creation_funcs.py
import random
from characters import CEO, Manager, CorporateSecurity, CorporateAssasin, Employee, Accountant
from location import HQ
from create_character_names import create_name
from motivation_presets import MotivationPresets

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
    ceo = CEO(
        name=create_name(None, random.choice(["Male", "Female"])),
        faction=faction,
        region=faction.region,
        location=corp_hq,
        initial_motivations=MotivationPresets.for_class("CEO")
    )
    faction.add_CEO(ceo)
    characters.append(ceo)

    # Managers
    for _ in range(random.randint(2, 3)):
        manager = Manager(
            name=create_name(None, random.choice(["Male", "Female"])),
            faction=faction,
            region=faction.region,
            location=corp_hq,
            initial_motivations=MotivationPresets.for_class("Manager")
        )
        faction.add_manager(manager)
        characters.append(manager)

    # Employees
    for _ in range(random.randint(3, 6)):
        employee = Employee(
            name=create_name(None, random.choice(["Male", "Female"])),
            faction=faction,
            region=faction.region,
            location=corp_hq,
            initial_motivations=MotivationPresets.for_class("Employee")
        )
        faction.add_employee(employee)
        characters.append(employee)

    # Security
    for _ in range(random.randint(2, 4)):
        guard = CorporateSecurity(
            name=create_name(None, random.choice(["Male", "Female"])),
            faction=faction,
            region=faction.region,
            location=corp_hq,
            initial_motivations=MotivationPresets.for_class("CorporateSecurity")
        )
        faction.add_security(guard)
        characters.append(guard)

    # Accountants
    for _ in range(random.randint(1, 3)):
        accountant = Accountant(
            name=create_name(None, random.choice(["Male", "Female"])),
            faction=faction,
            region=faction.region,
            location=corp_hq,
            initial_motivations=MotivationPresets.for_class("Accountant")
        )
        faction.add_accountant(accountant)
        characters.append(accountant)

    # Corporate Assassins
    for _ in range(random.randint(0, 2)):
        assassin = CorporateAssasin(
            name=create_name(None, random.choice(["Male", "Female"])),
            faction=faction,
            region=faction.region,
            location=corp_hq,
            initial_motivations=MotivationPresets.for_class("CorporateAssassin")
        )
        characters.append(assassin)

    return characters