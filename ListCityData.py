import os
import yaml

def list_files_in_directory(root_directory):
    """
    Recursively lists all files in the given directory, organizing them into a nested dictionary structure.

    :param root_directory: The root directory to start scanning.
    :return: A dictionary representing the folder structure.
    """
    file_structure = {}

    for root, dirs, files in os.walk(root_directory):
        # Create a nested structure for the current directory
        relative_path = os.path.relpath(root, root_directory)
        directory = relative_path if relative_path != '.' else os.path.basename(root_directory)

        file_structure[directory] = {
            "folders": sorted(dirs),
            "files": sorted([f for f in files if f.endswith((".py", ".yaml", ".json", ".csv", ".txt"))]),
        }

    return file_structure

def save_to_yaml(data, output_file):
    """
    Saves the given data to a YAML file.

    :param data: The data to save.
    :param output_file: The path to the output file.
    """
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Ensure the directory exists

    with open(output_file, 'w') as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=False, sort_keys=False)

if __name__ == "__main__":
    # Define the directory to scan and the output file
    root_directory = os.path.join("data", "Test City")
    output_file = os.path.join(root_directory, "TestCityFilesStructure.yaml")

    # Generate the file structure and save it
    try:
        file_structure = list_files_in_directory(root_directory)
        save_to_yaml(file_structure, output_file)
        print(f"File structure saved to: {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")
