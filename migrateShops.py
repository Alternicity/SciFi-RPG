import json
import os

# Ensure the working directory is set correctly
script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the script

# Directory containing shop JSON files
base_directory = os.path.join(script_dir, "data", "Test City", "Shops")
print(f"Resolved base directory: {base_directory}")

def migrate_shop_file(file_path):
    """Migrates a single shop data file to the new schema."""
    backup_path = file_path + ".backup"

    # Backup the original file
    if not os.path.exists(backup_path):
        print(f"Creating backup for {file_path}...")
        os.rename(file_path, backup_path)

    # Read the original data
    with open(backup_path, 'r') as file:
        shops = json.load(file)

    # Migrate data
    migrated_shops = []
    for shop in shops:
        shop.setdefault('legality', 'Legal')  # Default legality
        shop.setdefault('bankCardCash', 0)   # Default bank card cash
        shop.setdefault('cash', 0)           # Default cash

        # Convert items_available to inventory if present
        if 'items_available' in shop:
            shop['inventory'] = {
                item['item']: {
                    'price': item['price'],
                    'quantity': 10  # Default quantity
                } for item in shop.pop('items_available')
            }

        # Add defaults for 'fun' if it's a Shop
        if shop.get('type') == 'Shop':
            shop.setdefault('fun', 0)

        # Remove 'stored_items' if not applicable
        if shop.get('type') != 'Stash':
            shop.pop('stored_items', None)

        migrated_shops.append(shop)

    # Write the migrated data
    with open(file_path, 'w') as file:
        json.dump(migrated_shops, file, indent=4)

    print(f"Migration completed for {file_path}!")

def migrate_shops_in_directory(directory):
    """Migrates all shop files in the specified directory."""
    for file_name in os.listdir(directory):
        if file_name.endswith("_shops.json"):
            migrate_shop_file(os.path.join(directory, file_name))

# Example usage
migrate_shops_in_directory(base_directory)
