from location import HQ


def adjust_morale(characters, location):
    for character in characters:
        character.morale += location.fun


# Example Use Case
hq = HQ(name="Alpha HQ", side="East Side", security_level="High", condition="Well Maintained", fun=2)
shop = Shop(name="Gamma Store", side="West Side", security_level="Medium", condition="Clean", profit_margin=1.5, fun=1)

print(hq)
print(shop)