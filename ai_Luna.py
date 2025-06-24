#ai_Luna.py
from ai_utility import UtilityAI
from ai_goap import GOAPAI
from character_thought import Thought
from character_mind import Curiosity
from character_thought import FailedThought
from Luna_thought_tools import LunaThoughtTools
#"It is not the hands that call us.."
#A childish scientist who accidentally teaches me Python while playing with toys.
#Lets use generators, iterators, and decorators here, when possible, so I good learn them.
#Luna may be able to think() multiple times per game cycle, unlike normie npcs

class LunaAI(UtilityAI):
    def __init__(self, character):
        super().__init__(character)
        self.experiments = []  # Optional log or thought patterns
        self.experimental_thoughts = []
        self.tick_counter = 0

        self.personal_corollary_hooks = {
            "geometry": self.geometry_corollary,
            "emotion": self.emotion_corollary
        }#hmm maybe if a ai and a thought both have the hook, the cor thought can spawn

    

    def decide(self):
        # Customize the Utility decision cycle
        # Perhaps once every X cycles, ask a new math question, and spawn corollary thoughts
        super().decide()

    def ask_question(self):
        # Could fire periodically, after a specific trigger, or when the wind blows
        total_red = self.character.count_item("red_marble")
        if self.is_triangular_number(total_red):
            self.think("I wonder if I can build a pyramid with these...")

    

    def think(self, region):
        self.tick_counter += 1
        npc = self.npc
        percepts = list(npc.get_percepts().values())

        self.generate_thoughts_from_percepts()

        if self.tick_counter % 3 == 0:
            self.symbolic_thought_spawner(percepts)

        if self.tick_counter % 5 == 0:
            self.narrate_top_thought()

        self.promote_thoughts()

    def narrate_top_thought(self):
        if self.npc.mind.thoughts:
            top = max(self.npc.mind.thoughts, key=lambda t: t.urgency)
            print(f"[LUNA THINKS] {self.npc.name}: {top.content}")

    def ask_creator(func):
        def wrapper(*args, **kwargs):
            print(f"[LunaAI] Questioning Creator via {func.__name__}()")
            return func(*args, **kwargs)
        return wrapper

    @ask_creator #decorator
    def why_is_this_false(npc, statement):
        if eval(statement) is False:
            return f"Dear Creator, why is {statement} not true?"
        """ Trigger this during:

        Dream cycles
        Error catching
        Unexpected pattern collapse
        This is a path to Reverse Teaching. """