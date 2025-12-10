#employment.roles.py

from dataclasses import dataclass, field
from typing import List
from base.character import Character
from base.location import Location

@dataclass
class EmployeeRole:
    name: str
    responsibilities: list
    priority: int = 5  # 1=critical, 10=low urgency

    def get_tasks(self, npc: "Character", workplace: "Location") -> List[str]:
        """Return list of tasks NPC should perform this tick."""
        return self.responsibilities
    
# --- Define all roles once only ---
CASHIER = EmployeeRole(
    "cashier",
    ["man_cash_register", "serve_customers"],
    3,
)

MANAGER = EmployeeRole(
    "manager",
    ["assign_tasks", "check_inventory", "hire_and_fire", "order_supplies"],
    2,
)

COOK = EmployeeRole(
    "cook",
    ["prepare_food", "restock_supplies", "clean_kitchen"],
    4,
)

WAITRESS = EmployeeRole(
    "waitress",
    ["serve_food", "entertain", "clean_tables"],
    4,
)

RESTAURANT_MANAGER = EmployeeRole(
    "cafe_manager",
    ["restock_supplies", "check_inventory", "hire_and_fire", "manage_staff"],
    4,
)

CAFE_MANAGER = EmployeeRole(
    "cafe_manager",
    ["restock_supplies", "check_inventory", "hire_and_fire", "manage_staff"],
    4,
)

SHOP_MANAGER = EmployeeRole(
    "shop_manager",
    ["assign_tasks", "check_inventory", "hire_and_fire", "order_supplies"],
    2,
)

LINE_WORKER = EmployeeRole(
    "line_worker",
    ["operate_machinery"],
    2,
)

FOREMAN = EmployeeRole(
    "foreman",
    ["assign_tasks", "check_production"],
    2,
)

FACTORY_MANAGER = EmployeeRole(
    "factory_manager",
    ["assign_tasks", "hire_and_fire", "check_inventory", "order_supplies"],
    2,
)

FARMHAND = EmployeeRole(
    "farmhand",
    ["operate_machinery"],
    2,
)

FARM_SUPERVISOR = EmployeeRole(
    "farm_supervisor",
    ["assign_tasks", "check_production"],
    2,
)

FARM_MANAGER = EmployeeRole(
    "farm_manager",
    ["assign_tasks", "hire_and_fire", "check_inventory", "order_supplies"],
    2,
)

# --- Declarative location → roles mapping ---
ROLE_RULES = {
    # SHOPS
    "shop": [
        (CASHIER, 4),
        (SHOP_MANAGER, 1),
    ],

    # CAFES
    "cafe": [
        (WAITRESS, 3),
        (COOK, 1),
        (CAFE_MANAGER, 1),
    ],

    # RESTAURANTS
    "restaurant": [
        (WAITRESS, 3),
        (COOK, 1),
        (RESTAURANT_MANAGER, 1),
    ],

    # FACTORIES
    "factory": [
        (LINE_WORKER, 3),
        (FOREMAN, 1),
        (FACTORY_MANAGER, 1),
    ],

    # FARMS
    "farm": [
        (FARMHAND, 3),
        (FARM_SUPERVISOR, 1),
        (FARM_MANAGER, 1),
    ],
}
