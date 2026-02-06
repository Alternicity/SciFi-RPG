# tests/test_anchor_salience.py

# Run with
#.venv/bin/python -m pytest -q

import pytest
from anchor_visit import VisitToRobAnchor

from location_types import Shop
from character_mind import Mind


class DummyNPC:
    def __init__(self):
        self.name = "TestNPC"
        # minimal dummy Region and Mind for compatibility
        self.region = type("Region", (), {"name": "downtown"})()
        self.mind = type("Mind", (), {"memory": type("Memory", (), {"semantic": {}})})()
        # ↑ type(name, bases, dict) dynamically makes a temporary class
        #   e.g. type("Region", (), {"name": "downtown"})() creates
        #   an object of an anonymous class with attribute .name = "downtown"


class DummyLocation:
    def __init__(self, name, tags=None, robbable=False):
        self.name = name
        self.tags = tags or []
        self.robbable = robbable

    def get_percept_data(self, observer=None):
        return {"tags": self.tags, "object": self, "name": self.name}


def test_salience_from_percept_data():
    anchor = VisitToRobAnchor(name="visit_to_rob", type="motivation", weight=1.0)
    npc = DummyNPC()
    loc = DummyLocation("Shop", tags=["shop", "robbable", "ranged_weapon"], robbable=True)
    percept = loc.get_percept_data(observer=npc)

    score = anchor.compute_salience_for(percept, npc)
    assert score > 0, f"Expected positive salience, got {score}"
