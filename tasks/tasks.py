#tasks.py
import logging
from collections import deque

logging.basicConfig(level=logging.INFO)

class Task:
    """Small unit of accomplishment for npcs using utility AI."""

    VALID_DIFFICULTIES = ("easy", "medium", "hard")
    VALID_STATUSES = ("pending", "completed")

    def __init__(self, name, difficulty, duration=1, dependencies=None):
        """Initialize a task with the given attributes."""
        if difficulty not in self.VALID_DIFFICULTIES:
            raise ValueError(f"Invalid difficulty: {difficulty}. Must be one of {self.VALID_DIFFICULTIES}.")
        self.name = name
        self.difficulty = difficulty
        self.duration = duration
        self.time_remaining = duration
        self.dependencies = dependencies or []
        self.status = "pending"

    def can_start(self):
        """Check if the task can start (all dependencies completed)."""
        return all(dep.status == "completed" for dep in self.dependencies)

    def progress_task(self, time_elapsed):
        """Progress the task by the given time."""
        if self.status == "completed":
            logging.warning(f"Task '{self.name}' is already completed.")
            return
        if not self.can_start():
            logging.warning(f"Task '{self.name}' cannot start. Dependencies incomplete.")
            return
        self.time_remaining -= time_elapsed
        if self.time_remaining <= 0:
            self.complete_task()

    def complete_task(self):
        """Mark the task as completed."""
        self.status = "completed"
        logging.info(f"Task '{self.name}' is completed.")

    def __repr__(self):
        return f"<Task: {self.name} ({self.difficulty}, {self.status})>"
    
# This will be used per character
class TaskManager:
    def __init__(self, owner):
        self.owner = owner  # Reference to the Character
        self.queue = deque()
        self.current_task = None
        self.completed_tasks = []

    def add_task(self, task):
        self.queue.append(task)

    def get_next_task(self):
        if not self.current_task and self.queue:
            self.current_task = self.queue.popleft()
        return self.current_task

    def complete_current_task(self):
        if self.current_task:
            self.completed_tasks.append(self.current_task)
            self.current_task = None

    def interrupt_current_task(self): #Has the characters self.mind.attention_focus = None been hijacked?
        if self.current_task:
            self.queue.appendleft(self.current_task)
            self.current_task = None
            #use @attention_focus.setter