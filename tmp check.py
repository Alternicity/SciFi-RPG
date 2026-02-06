import csv

file_path = r"C:\Users\Stuart\Python Scripts\scifiRPG\data\Names\GermanNames.txt"

with open(file_path, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print(f"Row: {row}")  # Check each row structure
