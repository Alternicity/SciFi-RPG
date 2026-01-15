NARRATIVE_AXES = [
    "conflict_vs_harmony",
    "exploration_vs_consolidation",
    "self_vs_other",
    "truth_vs_illusion",
]
# the current paste is the sholw of this file. Should the above be encapsulated in a class, from the start?
#I will add plenty of other narrative attribute/fields over time, and functions, and subclasses.
#I want to avoid having to refactor this in the future if posssible, so want to get the structure fututre as proof as possible from the outset.
#I expect some elements to be stored in the game_state object as well, for later easy export - do you think that is wise?
#To create structure here, and logic, but store variables in game_state?
#Or should narrative variable storage be for some reason separate from game_state?
#And/or what about ECS style structuring?
#Should a narrative object/s be added to something as a component?
