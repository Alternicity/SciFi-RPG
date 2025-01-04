from display import print_region_data  # Import from display.py
from generators.generateRegions import generate_region  # Correct import statement


def get_valid_input(prompt, min_value, max_value):
    """Helper function to handle input validation for numeric inputs."""
    while True:
        try:
            value = int(input(prompt))
            if min_value <= value <= max_value:
                return value
            else:
                print(f"Please enter a number between {min_value} and {max_value}.")
        except ValueError:
            print(
                f"Invalid input. Please enter a number between {min_value} and {max_value}."
            )


def generate_region_menu():
    print("\nGenerate Region Configuration:")

    # Get user input for region size with numeric options
    print("\nChoose region size:")
    print("1. Small")
    print("2. Medium")
    print("3. Large")

    region_size_dict = {"1": "small", "2": "medium", "3": "large"}
    region_size = region_size_dict.get(input("Enter your choice (1, 2, or 3): "), None)

    if not region_size:
        print("Invalid input. Please choose 1, 2, or 3.")
        return

    # Get economic level
    economic_level = get_valid_input("Enter Economic Level (1-10): ", 1, 10)

    # Get danger level
    danger_level = get_valid_input("Enter Danger Level (1-10): ", 1, 10)

    # Generate the region
    try:
        region = generate_region(region_size, economic_level, danger_level)
    except Exception as e:
        print(f"Error generating region: {e}")
        return

    # Print the region data using the modular display function
    print_region_data(region)
