#objects.jewellery.py

from objects.InWorldObjects import ObjectInWorld

class Necklace(ObjectInWorld):
    def __init__(self):
        super().__init__(
            name="Necklace",
            toughness=1,
            item_type="jewellery",
            size="small",
            blackmarket_value=50,
            price=120,
            legality=True,
        )

        # Semantic tags (used later by appearance, charisma, social systems)
        self.tags = ["jewellery", "fashion", "charisma"]

        # Soft stats (not yet applied automatically)
        self.effects = {
            "charisma": +1
        }
        
    def get_percept_data(self, observer=None):
        return {
            "name": self.human_readable_id or self.name,
            "description": "A decorative necklace",
            "type": self.__class__.__name__,
            "origin": self,
            "urgency": 0,          # no immediate action pressure
            "source": None,
            "salience": 1,         # very low baseline
            "tags": self.tags + ["appearance"],
            "size": getattr(self, "size", "small"),
        }
