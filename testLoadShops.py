from loader import load_shops

try:
    shops = load_shops("North")
    print(f"Loaded shops: {shops}")
except Exception as e:
    print(f"Error: {e}")
