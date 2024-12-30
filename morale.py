from location import HQ


def adjust_morale(characters, location):
    for character in characters:
        character.morale += location.fun


