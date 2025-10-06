#ai_utils.py
from character_memory import MemoryEntry
from base_classes import Location
from typing import Optional

def encode_weapon_shop_memory(npc, shop: Location):
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
