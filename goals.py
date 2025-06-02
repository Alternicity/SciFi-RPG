import random
import logging
from tasks import Task

logging.basicConfig(level=logging.INFO)

#Deprecate objectives, Pause goals, Focus on tasks.py for npcs using utility

class Goal:
    """Represents a high-level goal for a faction. Although NPCs will generallz use Utility AI, I plan on eventually
    using GOAP for Gang Bosses, CEOs or corporations, and state VIPS"""
    
    VALID_GOALS = [
        "expand_territory",
        "maximise_profits",
        "eliminate_rivals",
        "fight the state",
        "increase_influence",
        "defend_assets",
        "acquire HQ", #for street gangs
        "monitor_streetgang_migration"
    ]

    OBJECTIVE_MAP = {
        "expand_territory": ["Secure nearby territory", "Eliminate Rival Patrols"],
        "maximise_profits": ["Increase black market Sales", "Acquire valuable items"],
        "eliminate_rivals": ["Attack Rival Strongholds", "Eliminate rival leaders"],
        "increase_influence": ["Recruit new members", "Establish alliances"],
        "defend_assets": ["Fortify key areas", "Protect valuable resources"],
    }

    def __init__(self, description, goal_type=None, priority=1, target=None, status="pending", ):
        """Initialize a goal with the given type."""
        self.goal_type = goal_type if goal_type in self.VALID_GOALS else random.choice(self.VALID_GOALS)
        self.description = description  # A short description of the goal
        self.priority = priority
        self.target = target  # Target entity or location (optional)
        self.status = status  # "pending", "in_progress", "completed", "failed"
        self.objectives = []
        self.generate_objectives()
        self.preconditions = []
        self.effects = []

    def add_precondition(self, condition):
        """Define when this goal should be selected in a GOAP system."""
        self.preconditions.append(condition)

    def add_effect(self, effect):
        """Define what happens when this goal is completed."""
        self.effects.append(effect)

    def update_status(self, new_status):
        """Update the goal's status."""
        if new_status in {"pending", "in_progress", "completed", "failed"}:
            self.status = new_status
            print(f"Goal updated to {new_status}.")
        else:
            print(f"Invalid status: {new_status}")

    def is_completed(self):
        """Check if the goal is completed."""
        #assign any credit or prestige
        return self.status == "completed"

    """ def goal_type():
        pass """

    def generate_objectives(self):
        """Generate specific objectives based on the goal_type."""
        self.objectives = self.OBJECTIVE_MAP.get(self.goal_type, ["Perform general tasks"])
        #logging.info(f"Generated objectives for goal '{self.goal_type}': {self.objectives}")

    def generate_tasks(self):
        """Convert objectives into tasks for NPCs."""
        tasks = []
        for objective in self.objectives:
            difficulty = random.choice(["easy", "medium", "hard"])
            task = Task(name=objective, difficulty=difficulty)
            tasks.append(task)
        return tasks

    def complete_goal(self):
        """Mark the goal as completed."""
        self.status = "completed"
        logging.info(f"Goal '{self.goal_type}' completed.")

    def generate_goal_templates():
        return [
            Goal(description="Expand territory", priority=1),
            Goal(description="Recruit new members", priority=3),
            Goal(description="Eliminate rival faction", priority=2),
        ]

    def generate_faction_goals(faction, current_events):
        goals = generate_goal_templates()
        customized_goals = []
        for goal in goals:
            if "rival" in goal.description and faction.type == "gang":
                goal.description += f" targeting {faction.get_top_rival()}"
            elif "territory" in goal.description:
                goal.target = faction.affiliation  # Use faction's own data
            customized_goals.append(goal)
        return customized_goals

    def fail_goal(self):
        """Mark the goal as failed."""
        self.status = "failed"
        logging.warning(f"Goal '{self.goal_type}' failed.")

def generate_goal_templates():
    return [
        Goal(description="Expand territory", goal_type="expand_territory"),
        Goal(description="Recruit new members", goal_type="increase_influence"),
        Goal(description="Eliminate rival faction", goal_type="eliminate_rivals"),
    ]

class FactionGoal(Goal):
    def __init__(self, description, priority=1, target=None, status="pending", faction=None):
        super().__init__(description, priority, target, status)
        self.faction = faction  # Which faction owns this goal

    def adapt_to_faction(self):
        """Customize the goal based on the faction's specifics."""
        if self.faction:
            self.description += f" for {self.faction.name}"
            # Modify based on faction priorities, rivals, etc.

    def __repr__(self):
        return f"<Goal(description='{self.description}', priority={self.priority}, status='{self.status}')>"