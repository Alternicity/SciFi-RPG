import os
import re
#Adjust the re.match regex if your class definitions include additional modifiers like decorators or comments.
def extract_class_names(file_path):
    """Extract class names from the given Python file."""
    class_names = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                # Match lines that start with "class ClassName"
                match = re.match(r'^\s*class\s+(\w+)', line)
                if match:
                    class_names.append(match.group(1))
    else:
        print(f"File not found: {file_path}")
    return class_names

def main():
    root_dir = os.getcwd()  # Assuming you run this from the root project directory
    files_to_scan = ["InWorldObjects.py", "weapons.py"]
    
    for file_name in files_to_scan:
        file_path = os.path.join(root_dir, file_name)
        print(f"\nClasses in {file_name}:")
        class_names = extract_class_names(file_path)
        if class_names:
            for name in class_names:
                print(f"  - {name}")
        else:
            print("  No classes found or file does not exist.")

if __name__ == "__main__":
    main()
