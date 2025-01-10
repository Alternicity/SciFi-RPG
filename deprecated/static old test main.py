# Test Items
pistol = ObjectInWorld(
    "Pistol",
    toughness="durable",
    damage_points=10,
    legality=True,
    legitimate_value=100,
    blackmarket_value=50,
    size="pocket_sized",
)
health_kit = ObjectInWorld(
    "Health Kit",
    toughness="fragile",
    damage_points=0,
    legality=True,
    legitimate_value=30,
    blackmarket_value=20,
    size="pocket_sized",
)

print("Items created:")
print(
    f"- {pistol.name}, toughness: {pistol.toughness}, value: {pistol.legitimate_value}"
)
print(
    f"- {health_kit.name}, toughness: {health_kit.toughness}, value: {health_kit.legitimate_value}"
)

# Characters
john = Character(
    name="John",
    char_role="Dealer",
    strength=10,
    agility=10,
    intelligence=10,
    luck=10,
    psy=10,
    toughness=10,
    morale=10,
    race="Terran",
    sex="male",
)
john.gang_membership = "Red"
print(
    f"\nCharacter created: {john.name}, role: {john.char_role}, gang: {john.gang_membership}"
)

lucy = Character(
    name="Lucy",
    char_role="CorporateEmployee",
    strength=10,
    agility=10,
    intelligence=10,
    luck=10,
    psy=10,
    toughness=10,
    morale=10,
    race="Terran",
    sex="female",
)
lucy.corporation = "Hannival"
lucy.status = "high"


# Stores
dealer_store = Dealer(
    name="Red Dealer", gang_affiliation="Red", cash=500, bankCardCash=1000
)
corporate_depot = CorporateDepot(
    name="Hannival Depot", corporation="Hannival", cash=1000, bankCardCash=5000
)
vendor_store = Vendor(name="City Vendor", cash=200, bankCardCash=300)

print(f"\nStores created:")
print(f"- {dealer_store.name}, gang affiliation: {dealer_store.gang_affiliation}")
print(f"- {corporate_depot.name}, corporation: {corporate_depot.corporation}")
print(f"- {vendor_store.name}, open to all customers")

# Inventory Setup
dealer_store.inventory.add_item(pistol)
corporate_depot.inventory.add_item(health_kit)

print("\nInitial inventories:")
print(f"- {dealer_store.name}:")
dealer_store.inventory.display_items()
print(f"- {corporate_depot.name}:")
corporate_depot.inventory.display_items()

# Test Transactions
print("\nTransactions:")
dealer_store.issue_item(john, pistol, price=100)  # Sale for non-gang member
corporate_depot.issue_item(lucy, health_kit)

vendor_store.inventory.add_item(pistol)
vendor_store.sell_item(john, pistol, base_price=100)
