#objects.unique_objects.py
from objects.InWorldObjects import ObjectInWorld, Laptop
from location.locations import Cafe
from weapons import Pistol

HotbedCafe = Cafe("Gossip Grounds")
HotbedCafe.is_hotbed = True

def hotbed_postprocess(data, observer):
    if getattr(HotbedCafe, "is_hotbed", False):
        data["hotbed"] = True
        data["tags"] = data.get("tags", []) + ["gossip", "popular"]
        data["description"] = f"{data.get('description', '')} This is a social hotspot."
    return data

HotbedCafe._postprocess_percept = hotbed_postprocess

class SecretLaptop(Laptop):
    def __init__(self):
        super().__init__()
        self.contains_mcguffin = True

    def _postprocess_percept(self, data, observer):
        if self.contains_mcguffin:
            data["tags"] = data.get("tags", []) + ["plot_critical"]
            data["description"] = "An unassuming laptop. But there's something... off."
        return data

class GoldPlatedPistol(Pistol):
    def __init__(self):
        super().__init__()
        self.is_gold_plated = True
        self.signals.extend([#here emits only once, no per percept cycle
            "wealth",
            "criminal",
            "luxury",
        ])

    def _postprocess_percept(self, data, observer):
        if self.is_gold_plated:
            data["gold_plated"] = True
            data["bling_level"] = "High"
            data["signals"] = self.get_signals()

        
        
        self.intimidation = 9
        blackmarket_value=350,
        #increase owner status if owner faction has semiotic bling
        return data