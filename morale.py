from location import HQ


def adjust_morale(characters, location):
    for character in characters:
        character.morale += location.fun


#morale measures a character's willingness to fight in a combat event
#and takes several factors into account.
#If a character fails a morale test, they run away and maybe cower or hide.