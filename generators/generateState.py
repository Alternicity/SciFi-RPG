from characters import VIP, RiotCop, Employee
from pathlib import Path

project_root = Path(__file__).parent.parent  # Adjust based on your directory structure
state_file_path = project_root / "data" / "Test City" / "Factions" / "TheState" / "state.json"

def generate_state(file_path=r"scifiRPG\data\Test City\Factions\TheState\state.json", tax_rate=0.15, num_riot_cops=10):
    """
    Generates or overwrites the state.json file with the State's details.

    Args:
        file_path (str): The path to save the State's JSON file.
        tax_rate (float): The tax rate applied by the State.
        num_riot_cops (int): The number of RiotCops to assign to the State.
    """
    state_name = "The State"

    # Ensure the State has at least one VIP
    vip = VIP(name="Governor", position="State Leader", influence=95, faction=state_name)

    # Generate RiotCops
    riot_cops = [
        RiotCop(name=f"RiotCop_{i+1}")
        for i in range(num_riot_cops)
    ]

    # Define the State's details
    state_data = {
        "name": state_name,
        "type": "faction",
        "affiliation": "none",
        "resources": 10000,
        "tax_rate": tax_rate,
        "laws": ["Maintain Order", "Enforce Taxes", "Prohibit Unlawful Activity"],
        "goals": [
            {"goal": "Maintain dominance over the region", "priority": "high", "reward": 2000},
            {"goal": "Generate tax revenue", "priority": "medium", "reward": 1500},
        ],
        "personnel": {
            "VIP": {
                "name": vip.name,
                "position": vip.position,
                "influence": vip.influence,
                "faction": vip.faction,
            },
            "RiotCops": [
                {"name": cop.name}
                for cop in riot_cops
            ],
        },
    }

    # Save the State data to a JSON file
    with open(file_path, "w") as file:
        json.dump(state_data, file, indent=4)
    print(f"State data saved to {file_path}")