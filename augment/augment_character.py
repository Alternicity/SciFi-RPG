#augment.augment_character.py

#buff packages for characters
#character Archtypes
#Guardian, Challenger, Mirror, Catalyst
from weapons import Knife
from objects.InWorldObjects import SmartPhone
from objects.jewellery import Necklace


from memory.injectors.initial_memory_injectors import inject_initial_social_memory
from social.social_utils import seed_social_relations

def augment_character(npc):
    """
    Called exactly once after npc.mind is created.
    Guarantees core cognitive subsystems exist.
    """

    # 1. Core semantic systems
    inject_initial_social_memory(npc)

    # 2. Optional early seeding (safe no-ops if nothing applies)
    seed_social_relations(npc)

    # 3. Future:
    # inject_loyalty_memory(npc)
    # inject_reputation_memory(npc)


def civilian_liberty_start(npc):
    npc.wallet.add_bankCardCash(300)
    npc.inventory.add_item(SmartPhone)

def civilian_waitress_start(npc):
    npc.inventory.add_item(Necklace)

    """ Injection = ensure structure exists
    Seeding = add initial content """