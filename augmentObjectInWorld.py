#augmentObjectInWorld.py
from weapons import Pistol
from location import Nightclub
from augmentObjectInWorld import Laptop
import types


#Instantiate an augmented object like this

GoldPistol = Pistol()
GoldPistol.is_gold_plated = True
def gold_postprocess(data, observer):
    if getattr(GoldPistol, "is_gold_plated", False):
        data["gold_plated"] = True
    return data
GoldPistol._postprocess_percept = gold_postprocess

#or

DangerClub = Nightclub("Gossip Grounds")
DangerClub.is_dangerousClub = True

def dangerousClub_postprocess(data, observer):
    if getattr(DangerClub, "is_dangerousClub", True):
        data["dangerousClub"] = True
        data["tags"] = data.get("tags", []) + ["gang", "popular"]
        data["description"] = f"{data.get('description', '')} This is a gangster club."
    return data

DangerClub._postprocess_percept = dangerousClub_postprocess

#or

SecretLaptop = Laptop()
SecretLaptop.secret_data = "Coordinates to secret base"

def secret_laptop_postprocess(self, data, observer):
    if getattr(self, "secret_data", None):
        data["mcguffin"] = True
        data["tags"].append("important")
        data["description"] += " (Looks ordinary, but seems significant)"
    return data

SecretLaptop._postprocess_percept = types.MethodType(secret_laptop_postprocess, SecretLaptop)

