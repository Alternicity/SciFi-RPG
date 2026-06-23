#perception.sublocation_percepts.py

from perception.perceptibility import (
    gather_perceptible_objects,
    extract_appearance_summary
)

""" def get_sublocation_percepts(sublocation):

    percepts = []

    for obj in sublocation.objects_present:
        
        for percept_obj in gather_perceptible_objects(obj):

            percepts.append(
                extract_appearance_summary(
                    percept_obj
                )
            )

    return percepts """

def get_sublocation_percepts(sublocation):

    percepts = []

    for obj in sublocation.objects_present:

        data = obj.get_percept_data()

        percepts.append(
            data.get(
                "description",
                obj.name
            )
        )


#old version
    """ for obj in sublocation.objects_present:

        print(
            "ROOT OBJECT:",
            type(obj).__name__,
            getattr(obj, "name", "NO_NAME")
        )

        for percept_obj in gather_perceptible_objects(obj):

            print(
                "PERCEPT OBJECT:",
                type(percept_obj).__name__,
                getattr(percept_obj, "name", "NO_NAME")
            )

            text = extract_appearance_summary(
                percept_obj
            )

            print(
                "SUMMARY:",
                text
            )

            percepts.append(text) """

    return percepts