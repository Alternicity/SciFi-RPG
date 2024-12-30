import logging
logging.basicConfig(level=logging.INFO)

class Task:
    """Represents a task in the simulation."""

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

    #from class subordinate 
    def receive_task(self, task):
        self.tasks.append(task)
        print(f"{self.name} is now handling task: '{task}'.")