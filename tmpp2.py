import os

directory = r"C:\Users\Stuart\Python Scripts\scifiRPG\data\Names"

for filename in os.listdir(directory):
    if filename.endswith(".txt"):  # Only check .txt files
        file_path = os.path.join(directory, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            first_lines = f.readlines()[:5]  # Read only the first few lines
            print(f"\n📂 {filename} - First 5 lines:")
            for line in first_lines:
                print(f"   {line.strip()}")