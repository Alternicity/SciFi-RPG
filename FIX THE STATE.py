import yaml

# Path to your YAML file
file_path = "data/the state.yaml"
formatted_path = "data/state_fixed.yaml"  # Save the fixed file

try:
    # Load the YAML file
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)

    # Write it back with proper formatting
    with open(formatted_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, indent=4)

    print(f"File formatted and saved to {formatted_path}")
except Exception as e:
    print(f"Error processing YAML: {e}")
