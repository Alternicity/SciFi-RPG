from InWorldObjects import ObjectInWorld
from base_classes import Character
from weapons import Weapon

import inspect

def get_all_subclasses(cls):
    subclasses = set()
    for subclass in cls.__subclasses__():
        subclasses.add(subclass)
        subclasses.update(get_all_subclasses(subclass))
    return subclasses

# Include base classes themselves
all_relevant_classes = {ObjectInWorld, Character, Weapon}
all_relevant_classes |= get_all_subclasses(ObjectInWorld)
all_relevant_classes |= get_all_subclasses(Character)
all_relevant_classes |= get_all_subclasses(Weapon)

missing_or_invalid = []

for cls in all_relevant_classes:
    method = getattr(cls, "get_percept_data", None)
    if not callable(method):
        missing_or_invalid.append(cls.__name__)
    else:
        try:
            source_lines = inspect.getsource(method)
            if "NotImplementedError" in source_lines:
                missing_or_invalid.append(cls.__name__ + " (NotImplementedError placeholder)")
        except OSError:
            # Built-in or C methods may raise this
            pass

print("Classes missing or with invalid get_percept_data():", missing_or_invalid)
