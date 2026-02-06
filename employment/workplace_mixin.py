#employment.workplace_mixin.py
from dataclasses import dataclass, field
from typing import List, Optional
from debug_utils import debug_print

class WorkplaceMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allowed_roles = []
        self.employees_there = []
        self.employees = []

        #The functions here look suspicious, and might be superfluous
    def add_employee(self, employee):#this function seemingly not called.
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

    def get_present_employees_at(location):#not called
        if hasattr(location, "workplace") and location.workplace:
            return location.workplace.employees_there
        return []

    # Renamed to avoid confusion with dormant 'task system'
    def get_duties_for_role(self, role):#called only in select_duty()
        return role.responsibilities  # these are 'duties' now

    def select_duty(self, employee):#Called only in run_workday_cycle
        duties = self.get_duties_for_role(employee.role)
        if not duties:
            return None
        # simple random or priority sort in future
        return duties[0]

    def perform_duty(self, employee, duty):
        # duty is a string like "serve_customers"
        # Future: dispatch to handler methods
        print(f"{employee.name} performs duty: {duty} at {self.name}")

    #do not call, violates utilityAI. Not called, deletion candidate
    def run_workday_cycle(self):
        """Called once per tick during work hours."""
        for employee in self.employees_there:
            duty = self.select_duty(employee)
            if duty:
                self.perform_duty(employee, duty)
