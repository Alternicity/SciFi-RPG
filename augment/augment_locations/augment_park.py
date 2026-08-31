#augment.augment_locations.augment_park.py
import random
from location.locations import Park, LunaSanctum
from objects.furniture import Table, Bench
from objects.trees_and_plants import GoldenRatioTree, Plant, Tree, OakTree, DustPalm, EchoWillow
from world.place_objects import place_object


def seed_park_objects(all_locations):
    #incorporate place_object()
    for loc in all_locations:
        if not isinstance(loc, Park):
            continue
        if isinstance(loc, LunaSanctum):
            continue  # Luna's park gets seeded separately. Unique sublocation to be later incorprated

        if any(isinstance(o, Tree) for o in loc.items.objects_present):
            continue
            #if any tree already exists, skip seeding.
            #Which is actually fine if the function is intended to be idempotent

        # Trees
       # 2-3 mundane trees
        mundane = [OakTree, DustPalm]
        for i, cls in enumerate(random.choices(mundane, k=3)):
            tree = cls()
            tree.name = f"{tree.name} {i+1}"

            place_object(tree, loc)

        # One special tree — sometimes GoldenRatio, sometimes EchoWillow
        special_cls = random.choice([GoldenRatioTree, EchoWillow])
        special = special_cls()
        place_object(special, loc)

        # Benches
        for i in range(4):
            bench = Bench(name=f"Park Bench {i+1}")
            place_object(bench, loc)

        loc.fun = min(8, 1 + sum(
            getattr(t, "resonance_factor", 1.0)
            for t in loc.items.objects_present
            if isinstance(t, Tree)
        ))

        # One special tree
        spiral = GoldenRatioTree()
        place_object(spiral, loc)

        # Ambient boost from trees