import os
import json

class FilePresetManager:
    def __init__(self, root_folder="Test City", file_types=[".json", ".py", ".txt"]):
        self.root_folder = root_folder
        self.file_types = file_types

    def list_presets(self):
        """Display current presets."""
        print("\nCurrent Presets:")
        print(f"Target Root Folder: {self.root_folder}")
        print(f"File Types: {', '.join(self.file_types)}\n")

    def modify_presets(self):
        """Interactive menu to modify presets."""
        while True:
            print("\nModify Presets:")
            print("1. Change Root Folder")
            print("2. Modify File Types")
            print("3. Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == "1":
                new_folder = input("Enter the new root folder: ").strip()
                if os.path.exists(new_folder):
                    self.root_folder = new_folder
                    print(f"Root folder updated to: {new_folder}")
                else:
                    print("Error: The folder does not exist.")
            elif choice == "2":
                print("\nCurrent File Types:", ", ".join(self.file_types))
                print("1. Add a File Type")
                print("2. Remove a File Type")
                sub_choice = input("Enter your choice: ")

                if sub_choice == "1":
                    new_type = input("Enter a new file type (e.g., .xml): ").strip()
                    if not new_type.startswith("."):
                        print("Error: File type must start with a dot (.)")
                    elif new_type in self.file_types:
                        print("Error: File type already exists.")
                    else:
                        self.file_types.append(new_type)
                        print(f"Added file type: {new_type}")
                elif sub_choice == "2":
                    print("Available File Types:", ", ".join(self.file_types))
                    remove_type = input("Enter the file type to remove: ").strip()
                    if remove_type in self.file_types:
                        self.file_types.remove(remove_type)
                        print(f"Removed file type: {remove_type}")
                    else:
                        print("Error: File type not found.")
                else:
                    print("Invalid option.")
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")

class FilePresetManager:
    def __init__(self, root_folder="Test City", file_types=[".json", ".py", ".txt"]):
        self.root_folder = root_folder
        self.file_types = file_types

    def list_presets(self):
        """Display current presets."""
        print("\nCurrent Presets:")
        print(f"Target Root Folder: {self.root_folder}")
        print(f"File Types: {', '.join(self.file_types)}\n")

    def modify_presets(self):
        """Interactive menu to modify presets."""
        while True:
            print("\nModify Presets:")
            print("1. Change Root Folder")
            print("2. Modify File Types")
            print("3. Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == "1":
                new_folder = input("Enter the new root folder: ").strip()
                if os.path.exists(new_folder):
                    self.root_folder = new_folder
                    print(f"Root folder updated to: {new_folder}")
                else:
                    print("Error: The folder does not exist.")
            elif choice == "2":
                print("\nCurrent File Types:", ", ".join(self.file_types))
                print("1. Add a File Type")
                print("2. Remove a File Type")
                sub_choice = input("Enter your choice: ")

                if sub_choice == "1":
                    new_type = input("Enter a new file type (e.g., .xml): ").strip()
                    if not new_type.startswith("."):
                        print("Error: File type must start with a dot (.)")
                    elif new_type in self.file_types:
                        print("Error: File type already exists.")
                    else:
                        self.file_types.append(new_type)
                        print(f"Added file type: {new_type}")
                elif sub_choice == "2":
                    print("Available File Types:", ", ".join(self.file_types))
                    remove_type = input("Enter the file type to remove: ").strip()
                    if remove_type in self.file_types:
                        self.file_types.remove(remove_type)
                        print(f"Removed file type: {remove_type}")
                    else:
                        print("Error: File type not found.")
                else:
                    print("Invalid option.")
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")


def list_city_data(directory, output_file): #is this code deprecated by the code above?
    # Ensure the directory exists
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return

    # File extensions to look for
    valid_extensions = {'.py', '.yaml', '.json', '.txt', '.csv'}

    # Gather files matching the valid extensions
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1] in valid_extensions:
                relative_path = os.path.relpath(os.path.join(root, file), directory)
                file_list.append(relative_path)

    # Write the list to the output file
    os.makedirs(directory, exist_ok=True)  # Ensure the output directory exists
    output_path = os.path.join(directory, output_file)
    with open(output_path, 'w') as f:
        f.write("Listing of files in 'Test City' directory:\n\n")
        f.write("\n".join(file_list))

    print(f"File list saved to {output_path}")


if __name__ == "__main__":
    # Define the directory and output file
    target_directory = r"C:\Users\Stuart\Python Scripts\scifiRPG\data\Test City"
    output_filename = "TestCityData.txt"

    # Generate the list
    list_city_data(target_directory, output_filename)

def display_directory_contents(self):
    """List files in the target root folder based on the file types."""
    print(f"\nListing files in '{self.root_folder}' with types {', '.join(self.file_types)}:")
    for root, _, filenames in os.walk(self.root_folder):
        for filename in filenames:
            if any(filename.endswith(ft) for ft in self.file_types):
                relative_path = os.path.relpath(os.path.join(root, filename), self.root_folder)
                print(relative_path)
    print()

# Usage Example
if __name__ == "__main__":
    # Specify the root directory to scan
    root_directory = "Test City"  # Replace with your actual directory
    list_files_in_directory(root_directory)