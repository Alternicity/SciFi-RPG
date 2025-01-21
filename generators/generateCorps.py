from distributions import generate_normal
from common import get_project_root, get_file_path
#ALL files use this to get the project root

def generate_corporations(economic_level, num_corporations=None):
    """
    Generate corporations based on the destination region's economic level, with variability in size and wealth.

    Args:
        economic_level (int): The economic strength of the region.
        num_corporations (int, optional): Specify the number of corporations to generate. 
            If not provided, it is calculated based on the economic level.

    Returns:
        list: A list of dictionaries containing corporation information.
    """
    if economic_level <= 0:
        raise ValueError("Economic level must be a positive integer.")

    # Determine the number of corporations if not explicitly provided
    num_corporations = num_corporations or max(1, int(generate_normal(mean=economic_level, std_dev=1.5)))

    corporations = []

    for i in range(num_corporations):
        # Calculate employees based on economic level with some variability
        employees = max(
            20,  # Minimum number of employees
            int(generate_normal(mean=50 * economic_level, std_dev=10))
        )

        # Calculate wealth based on economic level with some variability
        wealth = max(
            1000,  # Minimum wealth
            int(generate_normal(mean=10000 * economic_level, std_dev=2000))
        )

        # Append corporation details
        corporations.append({
            "name": f"Corporation {i + 1}",
            "economic_level": economic_level,
            "employees": employees,
            "wealth": wealth,
        })

    return corporations

# Example usage
if __name__ == "__main__":
    # Replace with the appropriate economic level for testing
    test_economic_level = 3
    generated_corporations = generate_corporations(economic_level=test_economic_level)
    for corp in generated_corporations:
        print(corp)
