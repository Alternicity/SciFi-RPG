#perception.sublocation_percepts.py

from perception.perceptibility import (
    gather_perceptible_objects,
    extract_appearance_summary
)

#function quarantined due to its scanning of objects_present, not getting this data from npc.percepts.values()
""" def get_sublocation_percepts(sublocation):

    percepts = []

    for obj in sublocation.objects_present:

        data = obj.get_percept_data()

        percepts.append(
            data.get(
                "description",
                obj.name
            )
        ) 

    return percepts"""