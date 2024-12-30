import random
import logging
from tasks import Task

logging.basicConfig(level=logging.INFO)

class Goal:
    """Represents a high-level goal for a faction."""

    VALID_GOALS = [
        "expand_territory",
        "maximise_profits",
        "eliminate_rivals",
        "increase_influence",
        "defend_assets",
    ]

    OBJECTIVE_MAP = {
        "expand_territory": ["Secure nearby territory", "Eliminate Rival Patrols"],
        "maximise_profits": ["Increase black market Sales", "Acquire valuable items"],
        "eliminate_rivals": ["Attack Rival Strongholds", "Eliminate rival leaders"],
        "increase_influence": ["Recruit new members", "Establish alliances"],
        "defend_assets": ["Fortify key areas", "Protect valuable resources"],
    }

    def __init__(self, goal_type=None):
        """Initialize a goal with the given type."""
        if goal_type is not None and goal_type not in self.VALID_GOALS:
            raise ValueError(f"Invalid goal_type: {goal_type}. Must be one of {self.VALID_GOALS}.")
        self.goal_type = goal_type if goal_type in self.VALID_GOALS else random.choice(self.VALID_GOALS)
        self.status = "active"
        self.objectives = []
        self.generate_objectives()

    def generate_objectives(self):
        """Generate specific objectives based on the goal_type."""
        self.objectives = self.OBJECTIVE_MAP.get(self.goal_type, ["Perform general tasks"])
        logging.info(f"Generated objectives for goal '{self.goal_type}': {self.objectives}")

    def generate_tasks(self):
        """Convert objectives into tasks."""
        tasks = []
        for objective in self.objectives:
            difficulty = random.choice(["easy", "medium", "hard"])
            tasks.append(Task(name=objective, difficulty=difficulty))
        return tasks

    def complete_goal(self):
        """Mark the goal as completed."""
        self.status = "completed"
        logging.info(f"Goal '{self.goal_type}' completed.")

    def fail_goal(self):
        """Mark the goal as failed."""
        self.status = "failed"
        logging.warning(f"Goal '{self.goal_type}' failed.")

    def __repr__(self):
        return f"Goal: {self.goal_type.capitalize()}, Status: {self.status}, Objectives: {self.objectives}"