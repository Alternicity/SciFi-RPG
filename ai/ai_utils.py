#ai.ai_utils.py
from character_memory import MemoryEntry
from base.location import Location
from base.character import Character
from anchors.anchor import Anchor
from worldQueries import location_sells_food, find_seller_employee
from debug_utils import debug_print
from character_thought import Thought

def resolve_contextual_focus(npc):
    #find other contextual stuff calls
    urgent = npc.motivation_manager.get_highest_priority_motivation()

    debug_print(
    npc,
    f"[MOTIVE DEBUG] {npc.name} "
    f"urgent={urgent.type if urgent else None} "
    f"urgency={urgent.urgency if urgent else None}",
    category="motive"
)

    hunger_thought = npc.mind.get_thought_with_tag("hunger")

    if urgent and urgent.type == "eat" and hunger_thought:#as per this dev push: "Motivation identity lives in .type"
        #find_food_seller(npc)
        pass
    


def encode_weapon_shop_memory(npc, shop: Location):#maybe move this logic to a seed block in simulation
    """
    Construct (but do NOT append) a MemoryEntry describing the shop selling ranged weapons.
    Caller should insert it into memory via add_semantic_unique() or add_semantic().
    Returns: MemoryEntry
    """


    details_text = f"{shop.name} sells ranged weapons"

    entry = MemoryEntry(
        subject=npc.name,
        object_=shop.name,
        verb="knows",
        details=details_text,
        tags=["shop", "weapon", "ranged_weapon"],
        target=shop,
        importance=3,
        type="knowledge",
        initial_memory_type="semantic",
        function_reference="encode_weapon_shop_memory",
        implementation_path="ai_utils.py",
    )

    # don't append here — return it so callers can insert via add_semantic_unique()
    """ Why return instead of append?
    Keeps encode_* functions pure (create entry only), and centralizes dedup logic in the Memory object via add_semantic_unique.
    Avoids double-adding or inconsistent add semantics across callers """
    
    return entry

# TODO: Consider replacing with KnownWeaponLocationMemory if multiple similar sources found

class DebugNPCRegistry:
    def __init__(self):
        self._by_role = {}

    def register(self, role, npc):
        if role in self._by_role:
            assert self._by_role[role] is not npc, (
                f"Debug role {role} already assigned"
            )
        self._by_role[role] = npc

    def values(self):
        return self._by_role.values()


def social_scan(npc):
    #Ensure the social graph node exists for anyone co-present
    loc = npc.location
    if not loc:
        return

    for other in loc.characters_there:
        if other is npc:
            continue

        # Ensure relation exists
        social = npc.mind.memory.semantic.get("social")
        social.get_relation(other)
        """It should:

        create relations
        initialize counters
        do nothing else

        It should not:
        create thoughts
        create motivations
        create anchors
        interpret intent """