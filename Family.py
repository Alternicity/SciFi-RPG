#Family.py
from dataclasses import dataclass, field
import random
from typing import List, Dict, Optional
from debug_utils import debug_print
from location.locations import House, ApartmentBlock
#from common import weighted_choice
from base.location import Location
from characters import Civilian

@dataclass
class Family:
    """Lightweight social unit tracking related civilians."""
    surname: str
    members: List['Civilian'] = field(default_factory=list)
    home: Optional['Location'] = None

    @property
    def adults(self) -> List['Civilian']:
        return [c for c in self.members if getattr(c, "age", 20) >= 18]

    @property
    def children(self) -> List['Civilian']:
        return [c for c in self.members if getattr(c, "age", 20) < 18]

    def add_member(self, civilian: 'Civilian'):
        if civilian not in self.members:
            self.members.append(civilian)
            civilian.family = self
            if "family" not in civilian.social_connections:
                civilian.social_connections["family"] = []
            civilian.social_connections["family"].append(self)

    "add update npc.loyalties code here"


def assign_families_and_homes(game_state):
    """
    Groups civilians into families based on surname,
    assigns each family a residential location,
    and links partners probabilistically.
    """
    civilians = getattr(game_state, "civilians", [])
    regions = getattr(game_state, "all_regions", [])
    all_residences = [loc for loc in getattr(game_state, "all_locations", [])
                      if isinstance(loc, (House, ApartmentBlock))]

    if not civilians or not all_residences:
        debug_print(None, "[FAMILY] No civilians or residences to assign.", "family")
        game_state.families = []
        return []

    # -------------------------------
    # 1. Group by family name
    # -------------------------------
    families_by_name: Dict[str, Family] = {}
    for civ in civilians:
        if not hasattr(civ, "name") or " " not in civ.name:
            continue
        surname = civ.name.split()[-1]
        family = families_by_name.setdefault(surname, Family(surname=surname))
        family.add_member(civ)

    debug_print(None, f"[FAMILY] Grouped {len(families_by_name)} family surnames.", "family")

    # -------------------------------
    # 2. Assign homes
    # -------------------------------
    unassigned_residences = all_residences.copy()
    random.shuffle(unassigned_residences)

    for family in families_by_name.values():
        if not unassigned_residences:
            debug_print(None, f"[FAMILY] Out of residences while placing family {family.surname}.", "family")
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
        #debug_print(None, f"[FAMILY] Placed {len(family.members)} {family.surname} members at {home.name}.",category=["placement", "family", "population"])

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

    # -------------------------------
    # 4. Store and return
    # -------------------------------
    families = list(families_by_name.values())
    game_state.families = families
    debug_print(None, f"[FAMILY] Assigned {len(families)} families.", "family")

    return families
# -------------------------------------------------------------
# PATCH D: FAMILY SHOP OWNERSHIP LINKAGE
# -------------------------------------------------------------

def link_family_shops(game_state):
    """
    Link families to shops that bear their surname in the shop name.
    Example: 'O'Sullivan's Store' -> Family('O'Sullivan')
    """

    families = getattr(game_state, "families", [])
    all_shops = getattr(game_state, "all_shops", [])
    if not families or not all_shops:
        debug_print(None, "[FAMILY_SHOPS] No families or shops to link.", "family")
        return

    # Index families by surname for faster lookup
    surname_map: Dict[str, Family] = {fam.surname.lower(): fam for fam in families}

    matches = 0
    for shop in all_shops:
        shop_name_lower = shop.name.lower()

        # Attempt to find a family whose surname appears at start of shop name
        for surname, fam in surname_map.items():
            if shop_name_lower.startswith(surname.lower()):
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

                debug_print(None, f"[FAMILY_SHOPS] Linked {fam.surname} to {shop.name}.", "family")
                break  # one shop = one family owner, avoid duplicates

    debug_print(None, f"[FAMILY_SHOPS] Linked {matches} shops to families.", "family")
    #often 0 or 1, 5 would be logical as 5 shops currently exist
