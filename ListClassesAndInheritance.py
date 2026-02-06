import ast
import yaml
import os

def extract_classes_and_inheritance(file_path, output_file):
    """
    Extract class names and their inheritance from a Python file and save it as YAML.

    Args:
        file_path (str): The path to the Python file to analyze.
        output_file (str): The output YAML file name.
    """
    # Read the file content
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Parse the Python file content to an AST
    tree = ast.parse(file_content)

    # Extract class names and inheritance
    class_info = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            base_classes = [base.id for base in node.bases if isinstance(base, ast.Name)]
            class_info.append({'class_name': class_name, 'inherits_from': base_classes})

    # Save the information to a YAML file
    with open(output_file, 'w') as yaml_file:
        yaml.dump(class_info, yaml_file, default_flow_style=False)

    print(f"Class overview saved to {output_file}")

def run_on_button_click():
    """
    Run when a button is clicked, asking the user to choose between listing InWorldObjects or Weapons classes.
    """
    # Ask the user to choose a file type
    print("Please choose an option:")
    print("1. List In World Game Object Classes")
    print("2. List Weapons Classes")
    choice = input("Enter the number (1 or 2): ")

    # Define the paths based on the user's choice
    if choice == '1':
        file_path = 'InWorldObjects.py'  # Use the filename directly
        output_file = 'InWorldObjectsOverview.yaml'
    elif choice == '2':
        file_path = 'weapons.py'  # Use the filename directly
        output_file = 'WeaponsOverview.yaml'

    else:
        print("Invalid choice. Please enter 1 or 2.")
        return

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"The file {file_path} does not exist. Please try again.")
        return

    # Extract classes and generate the YAML file
    extract_classes_and_inheritance(file_path, output_file)

# Run the script when you click a button or trigger the function
if __name__ == "__main__":
    run_on_button_click()
