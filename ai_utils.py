#ai_utils.py
from memory_entry import ShopsSellRangedWeapons
from base_classes import Location

def encode_weapon_shop_memory(location: Location) -> ShopsSellRangedWeapons:
    memory = ShopsSellRangedWeapons(location_name=location.name)
    memory.source = location
    print(f"[ENCODE] Encoding memory: {location.name} sells weapons.")
    return memory
# TODO: Consider replacing with KnownWeaponLocationMemory if multiple similar sources found
