import csv
import os

# Adjust this to your actual names directory
NAMES_DIR = r"C:\Users\Stuart\Python Scripts\scifiRPG\data\Names"

import csv

def load_names_from_csv(filepath):
    male_names = []
    female_names = []
    family_names = []
    
    current_category = None

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:  # Skip empty lines
                continue

            # Detect category headers
            if line.lower() == "male name":
                current_category = "male"
                continue
            elif line.lower() == "female name":
                current_category = "female"
                continue
            elif line.lower() == "family name":
                current_category = "family"
                continue

            # Add name to the correct list
            if current_category == "male":
                male_names.append(line)
            elif current_category == "female":
                female_names.append(line)
            elif current_category == "family":
                family_names.append(line)

    #print(f"DEBUG: Loaded {len(male_names)} male, {len(female_names)} female, {len(family_names)} family names from {filepath}")
    return male_names, female_names, family_names



def load_all_name_files():
    """Loads all name files from the NAMES_DIR."""
    all_names = {}

    for filename in os.listdir(NAMES_DIR):
        if filename.endswith(".txt"):  # Only process .txt files
            filepath = os.path.join(NAMES_DIR, filename)
            print(f"📂 Loading: {filename}")
            male, female, family = load_names_from_csv(filepath)
            all_names[filename] = {"male": male, "female": female, "family": family}

    return all_names


if __name__ == "__main__":
    print("🚀 Starting name file processing...")
    names_data = load_all_name_files()
    print("🎉 Name loading complete!")

    # Debug output (optional)
    for category, data in names_data.items():
        print(f"\n📜 {category}: {len(data['male'])} male, {len(data['female'])} female, {len(data['family'])} family names")
