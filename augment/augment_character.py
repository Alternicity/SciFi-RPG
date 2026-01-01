#augment.augment_character.py

#buff packages for characters
#character Archtypes
#Guardian, Challenger, Mirror, Catalyst
from weapons import Knife
from objects.InWorldObjects import SmartPhone#SmartPhone marked not accessed

def civilian_liberty_start(npc):
    npc.wallet.add_bankCardCash(300)
    npc.inventory.add_item(SmartPhone)#SmartPhone marked not defined

