#code cut from class Character during refactor
class Null():
    self.task_manager = None
    """ Should Tasks Be Stored in Memory?
    Yes, that makes a lot of sense — but with separation of concerns:
    Memory stores past and ongoing tasks for recall, journaling, or planning.
    tasks[] list should still exist for actively assigned or planned tasks (like a task queue). """

    def remember_task(self, task): #Remember your TOP task
            self.mind.memory.append({
                "type": "task",
                "name": task.name,
                "time": "now",  # or use game clock
                "status": task.status,
            })

    def receive_task(self, task):
            self.tasks.append(task)
            print(f"{self.name} is now handling task: '{task}'.")

