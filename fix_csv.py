import os
import csv

# Folder where your CSV files are stored
DATA_FOLDER = r"C:\Users\Stuart\Python Scripts\scifiRPG\data\Names"

# Exclude these files
EXCLUDED_FILES = {"GangNames.csv", "CorpNames.csv"}

# Function to clean CSV files
def clean_csv_file(filepath):
    fixed_rows = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        print(f"⚠️ EMPTY FILE: {filepath}")
        return

    # First row should be the header
    header = rows[0]
    expected_columns = len(header)

    for row in rows:
        if not row or len(row) != expected_columns:
            print(f"🔴 FIXING MALFORMED ROW in {os.path.basename(filepath)}: {row}")
            # Try to split/join based on known format
            row = [col.strip() for col in ",".join(row).split(",")]
            if len(row) != expected_columns:
                print(f"⚠️ Could not fully fix: {row}")
                continue  # Skip truly broken rows
        fixed_rows.append(row)

    # Save cleaned file
    clean_filepath = filepath.replace(".csv", "_cleaned.csv")
    with open(clean_filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(fixed_rows)

    print(f"✅ CLEANED: {os.path.basename(clean_filepath)}")

# Process all CSV files in the directory
for filename in os.listdir(DATA_FOLDER):
    if filename.endswith(".csv") and filename not in EXCLUDED_FILES:
        file_path = os.path.join(DATA_FOLDER, filename)
        print(f"📂 Processing: {filename}")
        clean_csv_file(file_path)

print("🎯 Cleaning complete. Check *_cleaned.csv files for results!")
