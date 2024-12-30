class SubLeader(Character):
    is_concrete = False
    # Base class for manager and captain
    def __init__(self, name, faction, **kwargs):
        super().__init__(name, faction=faction, **kwargs)  # Don't pass char_role
        self.task_list = []

    def add_task(self, task):
        print(f"{self.name} adds task: '{task}' to their task list.")
        self.task_list.append(task)

    def delegate_task(self, task, subordinates):
        # Convert task names to lowercase for case-insensitive matching
        # Use task.lower() to make the incoming task name lowercase.

        task_lower = task.lower()
        task_list_lower = [t.lower() for t in self.task_list]

        if task_lower not in task_list_lower:
            print(
                f"{self.name} cannot delegate task '{task}' because it's not in their task list."
            )
            return

        # Find the actual task name to remove from the task list
        task_actual = next(t for t in self.task_list if t.lower() == task_lower)

        for subordinate in subordinates:
            print(f"{self.name} delegates task '{task_actual}' to {subordinate.name}")
            subordinate.receive_task(task_actual)

        self.task_list.remove(task_actual)
        print(
            f"Task '{task_actual}' has been delegated amd removed from the task list."
        )