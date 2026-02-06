#Family.py
from dataclasses import dataclass, field
import random
from typing import List, Dict, Optional
from debug_utils import debug_print
from location.locations import House, ApartmentBlock
#from common import weighted_choice
from base.location import Location
from characters import Civilian
from base.character import Character
from economy.economy import Ownership
from create.create_game_state import get_game_state
from world.placement import place_character
game_state = get_game_state()

@dataclass
class Family:
    """Lightweight social unit tracking related civilians."""
    family_name: str
    members: List[Character] = field(default_factory=list)
    home: Optional['Location'] = None

    @property
    def adults(self) -> List['Civilian']:
        return [c for c in self.members if getattr(c, "age", 20) >= 18]

    @property
    def children(self) -> List['Civilian']:
        return [c for c in self.members if getattr(c, "age", 20) < 18]

    def add_member(self, character):
        social = character.mind.memory.semantic.get("social")
        if not social:
            raise RuntimeError(f"{character.name} has no SocialMemory")

        gs = get_game_state()

        for other in self.members:
            other_social = other.mind.memory.semantic.get("social")

            rel_a = social.get_relation(other)
            rel_a.record_interaction(
                hour=gs.hour,
                day=gs.day,
                valence=0,
                new_type="family"
            )

            rel_b = other_social.get_relation(character)
            rel_b.record_interaction(
                hour=gs.hour,
                day=gs.day,
                valence=0,
                new_type="family"
            )

        self.members.append(character)

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
        char.family = family


    debug_print(None, f"[FAMILY] Grouped {len(families_by_name)} family family_names.", "family")

    # 2. Assign homes
    # -------------------------------
    unassigned_residences = all_residences.copy()
    random.shuffle(unassigned_residences)

    for family in families_by_name.values():
        if not unassigned_residences:
            debug_print(
                None,
                f"[FAMILY] No residence for family {family.family_name} (homeless family)",
                category=["family", "housing", "warning"]
            )
            family.home = None
            for civ in family.members:
                civ.is_homeless = True
            continue


        locked_members = [c for c in family.members if getattr(c, "placement_locked", False)]

        if locked_members:
            target_region = locked_members[0].region
            region_residences = [
                r for r in unassigned_residences
                if r.region is target_region
            ]
            if region_residences:
                home = region_residences.pop()
                unassigned_residences.remove(home)
            else:
                home = unassigned_residences.pop()
        else:
            home = unassigned_residences.pop()


        family.home = home

        for civ in family.members:
            civ.residences = [home]
            civ.is_homeless = False
            #add civ to home.characters_there here?
            if getattr(civ, "placement_locked", False):
                continue

            place_character(civ, home)




 
    # -------------------------------
    # 3. Link partners (rough pass)
    # -------------------------------

    for family in families_by_name.values():
        adults = family.adults
        random.shuffle(adults)

        gs = get_game_state()

        for i in range(0, len(adults) - 1, 2):
            a, b = adults[i], adults[i + 1]

            social_a = a.mind.memory.semantic.get("social")
            social_b = b.mind.memory.semantic.get("social")

            if not social_a or not social_b:
                continue

            rel_ab = social_a.get_relation(b)
            rel_ab.record_interaction(
                hour=gs.hour,
                day=gs.day,
                valence=0,
                new_type="partner"
            )

            rel_ba = social_b.get_relation(a)
            rel_ba.record_interaction(
                hour=gs.hour,
                day=gs.day,
                valence=0,
                new_type="partner"
            )

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
                    member.mind.memory.semantic["procedures"].append(
                        {
                            "type": "family_business",
                            "business": shop,
                            "family": fam.family_name
                        }
                    )
                    #Do not force everything into SocialMemory
                    #SocialMemory = person ↔ person only.

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

def assign_initial_location_from_family(npc):
    family = getattr(npc, "family", None)
    home = getattr(family, "home", None) if family else None

    if home:
        npc.location = home
        location = npc.location
        location.characters_there.append(npc)#does this look like it enforces the neceesary invariant correctly?
        npc.region = npc.location.region #You  said this silently overrides region after it was set earlier. We didnt deal with this yet
        
        return True

    debug_print(
        npc,
        "[HOUSING] No family home assigned (homeless)",
        category=["family", "housing", "warning"]
    )

    npc.is_homeless = True
    game_state.homeless.append(npc)#append, or add? It is a list
    return False
