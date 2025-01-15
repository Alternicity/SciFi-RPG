import os
import json

# Simulate a function to test file opening
def test_file_opening(file_path):
    try:
        with open(file_path, "r") as file:
            content = file.read()
            print("File opened successfully. Content:")
            print(content)
    except FileNotFoundError:
        print(f"FileNotFoundError: The file was not found at {file_path}")
    except PermissionError:
        print(f"PermissionError: Permission denied for file {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
file_path = "C:/Users/Stuart/Python Scripts/scifiRPG/data/Test City/Regions/North.json"
test_file_opening(file_path)
