import os

NAMES_DIR = r"C:\Users\Stuart\Python Scripts\scifiRPG\data\Names"

def clean_text_file(filepath):
    """Removes empty lines and fixes encoding issues."""
    try:
        with open(filepath, "r", encoding="utf-8-sig") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]  # Remove blank lines
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")  # Write cleaned data
        
        print(f"✅ Cleaned: {filepath}")
    
    except Exception as e:
        print(f"❌ ERROR cleaning {filepath}: {e}")

def clean_all_files():
    """Scans and cleans all name files in the directory."""
    for filename in os.listdir(NAMES_DIR):
        if filename.endswith(".txt"):
            clean_text_file(os.path.join(NAMES_DIR, filename))

if __name__ == "__main__":
    print("🛠️ Cleaning all name files...")
    clean_all_files()
    print("🎉 Cleaning complete!")
