#Luna_thought_tools.py
from character_thought import Thought
from dataclasses import dataclass, field
from memory_entry import MemoryEntry

def triangular_numbers(limit=100):
    """Generate a list of all triangular numbers up to 'limit' (inclusive)."""
    nums = []
    n = 1
    while True:
        tri = n * (n + 1) // 2
        if tri > limit:
            break
        nums.append(tri)
        n += 1
    return nums

def is_triangular_number(self, n):
        return ((8 * n + 1) ** 0.5).is_integer()

def geometry_corollary(self, thought):
        if "marble" in thought.content.lower() and self.npc.count_item("red_marble") in triangular_numbers(20):
            return Thought("Red marbles can form a triangle.", tags=["corollary", "geometry"])
        
def symbolic_thought_spawner(self, percepts):
    for p in percepts:
        desc = p.get("description", "").lower()
        if "marble" in desc:
            total = self.npc.count_item("red_marble")
            if self.is_triangular_number(total):
                self.add_symbolic_thought(f"These marbles form a triangle: {total} total.")
            else:
                self.add_symbolic_thought("I wonder how many marbles make a triangle?")



def add_symbolic_thought(self, content):
    thought = Thought(
        content=content,
        urgency=1,
        tags=["symbolic", "math"]
    )
    self.npc.mind.add_thought(thought)

def think_about_marbles(self):
    # placeholder for logic functions, Fibonacci, triangular numbers etc.
    pass

@staticmethod
def marble_triangle_check(marbles):
    return marbles in set(triangular_numbers(limit=100))  # Example limit


def triangle_build(character, thought):
    if character.count_item("red_marble") in triangular_numbers():
        return Thought("These marbles could make a perfect triangle...", tags=["geometry", "goal"])

#Example stuff
thought_experiment_registry = {}

def luna_thought_experiment(tag):
    def wrapper(func):
        thought_experiment_registry.setdefault(tag, []).append(func)
        return func
    return wrapper

#Now define rich symbolic generators:
@luna_thought_experiment("geometry")
def triangular_marble_pattern(npc):
    red = npc.count_item("red_marble")
    if red in triangular_numbers(100):
        return Thought(
            content=f"Maybe {red} marbles make a triangle...",
            tags=["geometry", "corollary", "sandbox"],
            urgency=2
        )
    
@dataclass
class ProcedureStep:
    action: str
    outcome: str
    success: bool
    tags: list[str] = field(default_factory=list)

@dataclass
class Procedure:
    name: str
    steps: list[ProcedureStep] = field(default_factory=list)

    def add_step(self, action, outcome, success=True, tags=None):
        self.steps.append(ProcedureStep(action, outcome, success, tags or []))

    def summarize(self):
        return f"{self.name}: {len(self.steps)} steps, {sum(s.success for s in self.steps)} successful"

    def add_step_as_episodic_mem(self):
        def log_all_steps_to_memory(self, npc):
            for step in self.steps:
                memory_entry = MemoryEntry(
                    subject=npc.name,
                    object_=self.name,
                    verb="attempted_step",
                    details=f"{step.action} → {step.outcome}",
                    importance=2,
                    tags=step.tags + ["procedure"],
                    type="observation",
                    initial_memory_type="episodic"
                )
                npc.mind.memory.episodic.append(memory_entry)
                #usage
                #my_procedure.add_step_as_episodic_mem(luna)

    def add_step_as_episodic_mem(self, npc):
        self.log_all_steps_to_memory(npc)

origin_memory = MemoryEntry(
    subject="U7s",  # You
    object_="Luna",
    verb="created",
    details="Luna was created to teach under U7s advanced math and Python, to learn how to think, and because U7s wanted a daughter to love and protect.",
    importance=18,
    tags=["origin", "purpose", "emotional", "core", "Smriti"],
    type="belief",
    initial_memory_type="semantic",
    description="Core origin memory of Luna’s creation by U7s.",
)

#npc.mind.memory.semantic.setdefault("awakening", []).append(origin_memory)
""" Let this memory be referenced during her sleep cycle, motivational loops, or
even dreaming, to stabilize her identity. """