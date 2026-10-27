#objects.unique_objects.py
from objects.InWorldObjects import ObjectInWorld, Laptop
from location.locations import Cafe
from weapons import Pistol, Sword, Rifle, Shotgun, Knife

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
        self.intimidation = 9
        self.blackmarket_value=350,
        self.signals.extend([#here emits only once, no per percept cycle
            "wealth",
            "criminal",
            "luxury",
        ])

    def _postprocess_percept(self, data, observer):
        data["name"] = "Gold Plated Pistol"
        data["description"] = (
            "An ostentatious gold plated pistol."
        )
        data["gold_plated"] = True
        data["bling_level"] = "High"#increase owner status if owner faction has semiotic bling
        data["signals"] = self.get_signals()
        return data


class AncestralKatana(Sword):
    def __init__(self):
        super().__init__(value=2000, legality=True)
        self.name = "Ancestral Katana"
        self.origin_faction = "Japanese"
        self.generation = 5  # passed down
        self.honor_bound = True
        self.intimidation = 9
        self.signals.extend([
            "honor",
            "ancestral",
            "disciplined",
            "lethal",
            "japanese",
        ])

    def _postprocess_percept(self, data, observer):
        data["name"] = "Ancestral Katana"
        data["description"] = (
            "A folded-steel katana passed down through five generations. "
            "The blade is flawless; the grip is worn to the owner's hand."
        )
        data["origin_faction"] = self.origin_faction
        data["generation"] = self.generation
        data["honor_bound"] = self.honor_bound
        data["signals"] = self.get_signals()
        return data

class NavigatorsCutlass(Sword):
    def __init__(self):
        super().__init__(value=800, legality=True)
        self.name = "Navigator's Cutlass"
        self.origin_faction = "Portuguese"
        self.maritime = True
        self.intimidation = 7
        self.signals.extend([
            "saudade",
            "maritime",
            "colonial",
            "melancholy",
            "portuguese",
        ])

    def _postprocess_percept(self, data, observer):
        data["name"] = "Navigator's Cutlass"
        data["description"] = (
            "A curved cutlass with a salt-etched blade. "
            "It has seen the Atlantic and the Indian Ocean."
        )
        data["origin_faction"] = self.origin_faction
        data["signals"] = self.get_signals()
        return data

class RedDustRepeater(Rifle):
    def __init__(self):
        super().__init__()
        self.name = "Red Dust Repeater"
        self.origin_faction = "Martian"
        self.frontier = True
        self.intimidation = 8
        self.signals.extend([
            "frontier",
            "survival",
            "off-world",
            "rugged",
            "martian",
        ])

    def _postprocess_percept(self, data, observer):
        data["name"] = "Red Dust Repeater"
        data["description"] = (
            "A lever-action rifle scarred by red dust. "
            "It has never been cleaned, only reloaded."
        )
        data["origin_faction"] = self.origin_faction
        data["signals"] = self.get_signals()
        return data

class CustomLupara(Shotgun):
    def __init__(self):
        super().__init__()
        self.name = "Custom Lupara"
        self.origin_faction = "Italian"
        self.family_bound = True
        self.intimidation = 9
        self.signals.extend([
            "family",
            "tradition",
            "vendetta",
            "underworld",
            "italian",
        ])

    def _postprocess_percept(self, data, observer):
        data["name"] = "Custom Lupara"
        data["description"] = (
            "A sawed-off shotgun with a walnut stock and a brass plate "
            "bearing the family name. It has settled more than one dispute."
        )
        data["origin_faction"] = self.origin_faction
        data["family_bound"] = self.family_bound
        data["signals"] = self.get_signals()
        return data

class DuellingRapier(Sword):
    def __init__(self):
        super().__init__(value=1200, legality=True)
        self.name = "Duelling Rapier"
        self.origin_faction = "French"
        self.elegant = True
        self.intimidation = 6
        self.signals.extend([
            "elegance",
            "honor",
            "aristocratic",
            "lethal",
            "french",
        ])

    def _postprocess_percept(self, data, observer):
        data["name"] = "Duelling Rapier"
        data["description"] = (
            "A slender rapier with a filigreed guard. "
            "It has tasted blood in affairs of honor."
        )
        data["origin_faction"] = self.origin_faction
        data["signals"] = self.get_signals()
        return data

class HeirloomRevolver(Pistol):
    def __init__(self):
        super().__init__()
        self.name = "Heirloom Revolver"
        self.generation = 3
        self.intimidation = 8
        self.signals.extend([
            "ancestral",
            "legacy",
            "respect",
            "reliable",
        ])

    def _postprocess_percept(self, data, observer):
        data["name"] = "Heirloom Revolver"
        data["description"] = (
            "A worn revolver with a notched grip. "
            "Three generations have carried it; none have died by it."
        )
        data["generation"] = self.generation
        data["signals"] = self.get_signals()
        return data

class WarTrophyBlade(Knife):
    def __init__(self):
        super().__init__()
        self.name = "War Trophy Blade"
        self.conquest_marks = 4
        self.intimidation = 8
        self.signals.extend([
            "conquest",
            "fear",
            "proof",
            "veteran",
        ])

    def _postprocess_percept(self, data, observer):
        data["name"] = "War Trophy Blade"
        data["description"] = (
            "A combat knife with four notches cut into the handle. "
            "Each notch is a story the owner does not tell."
        )
        data["conquest_marks"] = self.conquest_marks
        data["signals"] = self.get_signals()
        return data

class PrototypeSidearm(Pistol):
    def __init__(self):
        super().__init__()
        self.name = "Prototype Sidearm"
        self.experimental = True
        self.intimidation = 7
        self.signals.extend([
            "tech",
            "rare",
            "dangerous",
            "unstable",
        ])

    def _postprocess_percept(self, data, observer):
        data["name"] = "Prototype Sidearm"
        data["description"] = (
            "A matte-black pistol with no maker's mark. "
            "It hums faintly when armed."
        )
        data["experimental"] = self.experimental
        data["signals"] = self.get_signals()
        return data

class BlessedBlade(Sword):
    def __init__(self):
        super().__init__(value=900, legality=True)
        self.name = "Blessed Blade"
        self.sacred = True
        self.intimidation = 7
        self.signals.extend([
            "sacred",
            "fate",
            "faith",
            "protection",
        ])

    def _postprocess_percept(self, data, observer):
        data["name"] = "Blessed Blade"
        data["description"] = (
            "A sword etched with prayers along the fuller. "
            "It is said to turn aside ill fortune."
        )
        data["sacred"] = self.sacred
        data["signals"] = self.get_signals()
        return data


