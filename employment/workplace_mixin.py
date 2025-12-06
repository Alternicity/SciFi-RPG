#employment.workplace_mixin.py
from dataclasses import dataclass, field
from typing import List, Optional
from debug_utils import debug_print
@dataclass
class WorkplaceMixin:
    """Mixin for Location classes that can employ characters."""
    
    allowed_roles: List = field(default_factory=list)
    employees_there: list = field(default_factory=list)    # currently present
    employees: list = field(default_factory=list)      # permanent employees

    def add_employee(self, employee):
        if employee not in self.employees:
            self.employees.append(employee)
            """ You do not add the employee to employees_there here
            That list is used ONLY when NPCs arrive for their shift
            That will be handled later inside the tick loop """

        # character’s own profile already stores workplace
        employee.employment.workplace = self

        debug_print(
            npc=employee,
            message=f"[EMPLOYMENT] Added {employee.name} to {self.name} staff",
            category="employment"
        )

    # Renamed to avoid confusion with dormant 'task system'
    def get_duties_for_role(self, role):
        return role.responsibilities  # these are 'duties' now

    def select_duty(self, employee):
        duties = self.get_duties_for_role(employee.role)
        if not duties:
            return None
        # simple random or priority sort in future
        return duties[0]

    def perform_duty(self, employee, duty):
        # duty is a string like "serve_customers"
        # Future: dispatch to handler methods
        print(f"{employee.name} performs duty: {duty} at {self.name}")

    def run_workday_cycle(self):
        """Called once per tick during work hours."""
        for employee in self.employees_there:
            duty = self.select_duty(employee)
            if duty:
                self.perform_duty(employee, duty)
