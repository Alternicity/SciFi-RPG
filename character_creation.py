import logging
from characters import (Boss, Captain, Employee, VIP, RiotCop,
                         CorporateAssasin, Employee, GangMember,
                           CEO, Manager, CorporateSecurity, Civilian)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def create_characters_as_objects():
    logging.info("Creating characters as objects..")
    characters = [
        VIP(name="Jurgen", bankCardCash=10000, faction="The State"),
        Manager(name="Carolina", faction="BlueCorp", bankCardCash=500),
        #CorporateAssasin(name="Jane", faction="BlueCorp"),
        #Civilian(name="Vihaan", bankCardCash), # ATTN!
        #CorporateSecurity(name="John", faction="BlueCorp"),
        RiotCop(name="Cletus", faction="The State"),
        #CEO(name="Terrence", faction="BlueCorp"),
        #Boss(name="Soren", faction="White Gang"),
        #Captain(name="Sven", faction="White Gang"),
        #GangMember(name="Swiz", faction="White Gang"),
        #Employee(name="Susana", faction="BlueCorp"),
        
    ]
    return characters