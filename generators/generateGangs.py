from distributions import generate_normal

from common import get_project_root, get_file_path
#ALL files use this to get the project root

def generate_gangs(danger_level: int):
    """
    Generate gang data with variability in the number of gangs and their members.
    Args:
        danger_level (int): The overall danger level of the region
    Returns:
        list: A list of dictionaries containing gang information.
    """
    num_gangs = max(1, int(generate_normal(mean=danger_level / 2, std_dev=2)))  # Variable gang count
    gangs = []
    
    for i in range(num_gangs):
        members = max(5, int(generate_normal(mean=10 + danger_level, std_dev=3)))  # Variable member count
        gangs.append({
            "name": f"Gang {i+1}",
            "danger_level": danger_level,
            "members": members,
        })
    
    return gangs
