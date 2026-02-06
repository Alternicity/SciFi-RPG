import os

# Define the root folder and file extensions to look for
root_folder = r"/home/stuart/SciFi-RPG"
extensions = {'.py', '.yaml', '.json'}
output_file = "file_structure.txt"  # Output file name

# Placeholder for the output structure
file_structure = []

# Walk through the root folder
for dirpath, dirnames, filenames in os.walk(root_folder):
    # Exclude any directory named '.venv' (at any depth) and '.git'
    if '.venv' in dirpath.split(os.sep) or '.git' in dirpath.split(os.sep):
        continue  

    # Get relative path for better readability
    rel_path = os.path.relpath(dirpath, root_folder)
    rel_path = "." if rel_path == "." else f"./{rel_path}"
    file_structure.append(f"Directory: {rel_path}")

    # Add files with specified extensions
    for filename in filenames:
        if os.path.splitext(filename)[1].lower() in extensions:
            file_structure.append(f"  - {filename}")

# Prepare the output as a single string
output_text = "\n".join(file_structure)

# Write the output to a file (overwrite mode)
with open(output_file, 'w', encoding="utf-8") as f:
    f.write(output_text)

print(f"File structure saved to {output_file}")
