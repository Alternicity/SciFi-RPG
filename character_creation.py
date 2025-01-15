import logging
from characters import (Boss, Captain, Employee, VIP, RiotCop,
                         CorporateAssasin, Employee, GangMember,
                           CEO, Manager, CorporateSecurity, Civilian)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def create_characters_as_objects():
    logging.info("Creating characters as objects..")
    characters = [
        #VIP(name="Jurgen", bankCardCash=10000, faction="The State", fun=1, hunger=2),
        Manager(name="Carolina", faction="BlueCorp", bankCardCash=500, fun=1, hunger=3),
        #CorporateAssasin(name="Jane", faction="BlueCorp", bankCardCash=10000, fun=0, hunger=1),
        #Civilian(name="Vihaan", bankCardCash=100, faction="Nonce", fun=0, hunger=7),
        #CorporateSecurity(name="John", faction="BlueCorp", bankCardCash=200, fun=0, hunger=4),
        #RiotCop(name="Cletus", faction="The State", bankCardCash= 125, fun=1, hunger=4),
        #CEO(name="Terrence", faction="BlueCorp", bankCardCash=10000, fun=5, hunger=0),
        #Boss(name="Soren", faction="White Gang", bankCardCash=3000, fun=3, hunger=1),
        #Captain(name="Sven", faction="White Gang", bankCardCash=200, fun=2, hunger=1),
        #GangMember(name="Swiz", faction="White Gang", bankCardCash=50, fun=1, hunger=3),
        #Employee(name="Susana", faction="BlueCorp", bankCardCash=100, fun=0, hunger=4),
        
    ]
    return characters