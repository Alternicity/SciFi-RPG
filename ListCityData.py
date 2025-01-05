import os

def list_city_data(directory, output_file):
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
    target_directory = r"C:\Users\Stuart\Python Scripts\scifi RPG\data\Test City"
    output_filename = "TestCityData.txt"

    # Generate the list
    list_city_data(target_directory, output_filename)
