# Validate and parse shop data
    for shop_data in shops_data:
        if not validate_shop_data(shop_data):
            raise ValueError(f"Invalid shop data: {shop_data}")


    # Parse shop data and create shop objects
    shops = []
    for shop_data in shops_data:
        if shop_data["type"] == "Shop":
            shop = Shop(
                name=shop_data["name"],
                inventory=shop_data["inventory"],
                cash=shop_data["cash"],
                bankCardCash=shop_data["bankCardCash"],
                legality=shop_data["legality"],
                security=shop_data["security"]
            )
        elif shop_data["type"] == "CorporateStore":
            shop = CorporateStore(
                name=shop_data["name"],
                corporation=shop_data["corporation"],
                inventory=shop_data.get("inventory", {}),
                cash=shop_data.get("cash", 0),
                bankCardCash=shop_data.get("bankCardCash", 0),
                legality=shop_data.get("legality", "Legal"),
                security=shop_data.get("security", Security())
            )
        elif shop_data["type"] == "Stash":
            shop = Stash(
                name=shop_data["name"],
                inventory=shop_data["inventory"],
                cash=shop_data["cash"],
                bankCardCash=shop_data["bankCardCash"],
                legality=shop_data["legality"],
                security=shop_data["security"]
            )
        shops.append(shop)

    #logger.info(f"Successfully loaded {len(shops)} shops for region '{region_name}'.")
    return shops

def validate_shop_data(shop_data: dict) -> bool:
    """
    Validates a single shop entry from the JSON data.
    Returns True if valid, False otherwise.
    """
    required_keys = {"type", "name", "inventory", "cash", "bankCardCash", "legality", "security"}
    missing_keys = required_keys - shop_data.keys()
    if missing_keys:
        logger.error(f"Shop entry is missing required keys: {missing_keys}")
        return False
    
    if shop_data["type"] == "CorporateStore" and "corporation" not in shop_data:
        logger.error(f"CorporateStore entry missing 'corporation': {shop_data}")
        return False
    else:
        return True

    # Additional validation logic (e.g., value types, ranges)
    if not isinstance(shop_data["inventory"], list):
        logger.error(f"'inventory' must be a list: {shop_data}")
        return False
    return True