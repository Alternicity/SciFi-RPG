# tmp_debug_print.py

from location.locations import Nightclub

def debug_print_nightclubs(all_locations):

    for loc in all_locations:

        if not isinstance(loc, Nightclub):
            continue

        print()
        print("=" * 60)
        print("CLUB:", loc.name)

        """ print("Objects in club:")
        for obj in loc.items.objects_present:
            print(" ", obj.name) """

        print("Sublocations:")
        for sub in loc.sublocations:

            print(" ", sub.name)

            if hasattr(sub, "items"):
                print(
                    "    objects:",
                    len(sub.items.objects_present)
                )