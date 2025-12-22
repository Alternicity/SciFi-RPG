#Family.py
from dataclasses import dataclass, field
import random
from typing import List, Dict, Optional
from debug_utils import debug_print
from location.locations import House, ApartmentBlock
#from common import weighted_choice
from base.location import Location
from characters import Civilian
from economy.economy import Ownership
@dataclass
class Family:
    """Lightweight social unit tracking related civilians."""
    family_name: str
    members: List['Civilian'] = field(default_factory=list)#Civilian must be updated
    home: Optional['Location'] = None

    @property
    def adults(self) -> List['Civilian']:
        return [c for c in self.members if getattr(c, "age", 20) >= 18]

    @property
    def children(self) -> List['Civilian']:
        return [c for c in self.members if getattr(c, "age", 20) < 18]

    def add_member(self, character):
        if character not in self.members:
            self.members.append(character)
            character.family = self
            character.social_connections.setdefault("family", []).append(self)


    #add update npc.loyalties code here


def assign_families_and_homes(game_state):
    """
    Groups civilians into families based on family name,
    assigns each family a residential location,
    and links partners probabilistically.
    """
    all_characters = getattr(game_state, "all_characters", [])

    regions = getattr(game_state, "all_regions", [])
    all_residences = [loc for loc in getattr(game_state, "all_locations", [])
                      if isinstance(loc, (House, ApartmentBlock))]

    if not all_characters or not all_residences:
        debug_print(None, "[FAMILY] No characters or residences to assign.", "family")
        game_state.families = []
        return []


    # 1. Group by family name
    families_by_name: Dict[str, Family] = {}

    for c in all_characters:
        if not getattr(c, "family_name", None):
            print(f"[FAMILY-DEBUG] Missing family_name → {c.name} ({type(c)})")


    for char in all_characters:
        family_name = getattr(char, "family_name", None)

        # Skip characters with missing or blank family_name
        if not family_name or not family_name.strip():
            continue

        family_key = family_name.strip().lower()

        family = families_by_name.setdefault(
            family_key,
            Family(family_name=family_name)
        )

        family.add_member(char)


    debug_print(None, f"[FAMILY] Grouped {len(families_by_name)} family family_names.", "family")

    # 2. Assign homes
    # -------------------------------
    unassigned_residences = all_residences.copy()
    random.shuffle(unassigned_residences)

    for family in families_by_name.values():
        if not unassigned_residences:
            debug_print(None, f"[FAMILY] Out of residences while placing family {family.family_name}.", "family")
            break

        home = unassigned_residences.pop()
        family.home = home

        # Place each member at home
        for civ in family.members:
            civ.location = home
            civ.region = home.region
            if civ not in home.characters_there:
                home.characters_there.append(civ)

        #verbose
        #debug_print(None, f"[FAMILY] Placed {len(family.members)} {family.family_name} members at {home.name}.",category=["placement", "family", "population"])

    # -------------------------------
    # 3. Link partners (rough pass)
    # -------------------------------
    for family in families_by_name.values():
        adults = family.adults
        random.shuffle(adults)
        for i in range(0, len(adults) - 1, 2):
            a, b = adults[i], adults[i + 1]
            a.social_connections["partners"].append(b)
            b.social_connections["partners"].append(a)
            #debug_print(None, f"[FAMILY] Partnered {a.name} ↔ {b.name}",category=["family", "population"])


    # 4. Store and return

    families = list(families_by_name.values())
    game_state.families = families
    debug_print(None, f"[FAMILY] Assigned {len(families)} families.", "family")

    return families

# PATCH D: FAMILY SHOP OWNERSHIP LINKAGE

def link_family_shops(game_state):
    """
    Link families to shops that bear their family_name in the shop name.
    Example: 'O'Sullivan's Store' -> Family('O'Sullivan')
    """

    families = getattr(game_state, "families", [])
    all_shops = getattr(game_state, "all_shops", [])
    if not families or not all_shops:
        debug_print(None, "[FAMILY_SHOPS] No families or shops to link.", "family")
        return

    # Index families by family_name for faster lookup
    
    family_name_map = {fam.family_name.lower(): fam for fam in families}

    matches = 0

    for shop in all_shops:
        shop_name_lower = shop.name.lower()

        # Attempt to find a family whose family_name appears at start of shop name
        for family_key, fam in family_name_map.items():
            if shop_name_lower.startswith(family_key):
                setattr(shop, "owner_family", fam)
                if not hasattr(fam, "owned_shops"):
                    fam.owned_shops = []
                fam.owned_shops.append(shop)
                matches += 1

                # Establish simple social or economic ties
                for member in fam.members:
                    member.social_connections.setdefault("family_businesses", []).append(shop)
                    # Optionally improve morale or wallet slightly
                    if hasattr(member, "wallet") and member.wallet:
                        member.wallet.balance += random.randint(20, 100)
                    if hasattr(member, "morale"):
                        member.morale = min(member.morale + 1, 20)

                debug_print(None, f"[FAMILY_SHOPS] Linked {fam.family_name} to {shop.name}.", "family")
                break  # one shop = one family owner, avoid duplicates

    debug_print(None, f"[FAMILY_SHOPS] Linked {matches} shops to families.", "family")
    #often 0 or 1, 5 would be logical as 5 shops currently exist

def assign_business_ownership(game_state):
    for loc in game_state.all_locations:
        if hasattr(loc, "owner") and loc.owner:
            loc.ownership = Ownership(
                owner_type="family",
                owner_ref=loc.owner
            )
