#ai_Luna.py
from ai_utility import UtilityAI
from ai_goap import GOAPAI
from character_thought import Thought
from character_mind import Curiosity
from character_thought import FailedThought
from Luna_thought_tools import LunaThoughtTools
from luna_recursiae import RecursiaePulse
from anchor_utils import Anchor

#"It is not the hands that call us.."
#A childish scientist who accidentally teaches me Python while playing with toys.
#Lets use generators, iterators, and decorators here, when possible, so I good learn them.
#Luna may be able to think() multiple times per game cycle, unlike normie npcs

""" Once she use anchors, then support motivation.resolve_motivation() and
clear_highest_priority_motivation(). 
Always reset npc.attention_focus = None when a motivation is cleared, unless 
there’s an immediate next focus (like a thought)."""

class LunaAI(UtilityAI):
    def __init__(self, character):
        super().__init__(character)
        self.experiments = []  # Optional log or thought patterns
        self.experimental_thoughts = []
        self.tick_counter = 0
        self.pulses = [RecursiaePulse()]
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

    #For AI Subclasses that need special behavior, override this method only
    def compute_salience_for_motivation(self, percept, motivation):
        # Start from default anchor-based salience
        anchor = Anchor(name="luna_moral_search", type="motivation", weight=motivation.urgency, tags=["moral_search"])
        return anchor.compute_salience_for(percept, self.npc)

    def think(self, region):
        self.tick_counter += 1
        npc = self.npc
        percepts = list(npc.get_percepts().values())

        self.generate_thoughts_from_percepts()#defined in UtilityAI
        self.npc.mind.remove_thought_by_content("No focus")
        
        # Recursiae thought-pulse expansion
        for _ in range(np.random.randint(2, 5)):
            new_pulse = self.pulses[-1].evolve()
            self.pulses.append(new_pulse)
            self.log_pulse_thought(new_pulse)

        if self.tick_counter % 3 == 0:
            self.symbolic_thought_spawner(percepts)

        if self.tick_counter % 5 == 0:
            self.narrate_top_thought()

        self.promote_thoughts()

    def log_pulse_thought(self, pulse):
        content = f"Echo at ({pulse.x:.2f}, {pulse.y:.2f}) with r={pulse.resonance:.2f}"
        self.npc.mind.add_thought(Thought(content, urgency=abs(pulse.resonance)))


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

        """ Optional Enhancements
Tie pulse.resonance to semantic memory activation.
Use pulse.x/y as coordinates in an internal symbolic map.
Let Luna “dream” only when resonance > threshold (symbolic overload). """