for i, (key, v) in enumerate(npc.percepts.items()):#not actually using location.characters.there

        # Step 1: Safely access nested data
        data = v.get("data", {})
        origin = v.get("origin", data.get("origin", "—"))

        # Step 2: Get description/type
        desc = data.get("description") or data.get("type") or "UNKNOWN"

        type_ = data.get("type", "—")
        
        # Remove redundant ": Type" or "(Type)" if it matches the actual type
        if isinstance(desc, str) and type_ in desc:
            desc = desc.replace(f": {type_}", "").replace(f"({type_})", "").strip()

        # Simplify verbose character description
        if isinstance(desc, str) and "," in desc and " of " in desc:
            desc = desc.split(",")[0]

        # NEW: Add controlling faction to location descriptions
        origin = v.get("origin", data.get("origin", "—"))

        if type_ == "Location" and isinstance(origin, Location):
            faction = getattr(origin, "controlling_faction", None)
            if faction:
                desc = f"{origin.name}, {faction.name}"
            else:
                desc = origin.name

        # Step 3: Replace origin with Appearance summary
        if origin != "—":
            appearance = extract_appearance_summary(origin)
        else:
            appearance = "[MISSING]"

        # Step 4: Count keys inside data block
        n_keys = len(data.keys())


        origin = v.get("origin") or data.get("origin")
        source = v.get("source", "UNKNOWN")

        # --- Unified, safe salience computation ---
        # Display is now anchor-centric: salience depends on the current anchor only.
        try:
            salience_score = anchor.compute_salience_for(origin, npc) if anchor else 0.0
        except Exception:
            salience_score = 0.0

                # --- Build Info Column ---
        info = "—"

        # Origin objects may be Location, Character, Item, etc.
        origin_obj = origin

        # Civilians
        if isinstance(origin_obj, Civilian):
            if getattr(origin_obj, "workplace", None) == npc.location:
                info = "Employee"
            else:
                info = "Civilian"

        # Gang Members
        elif isinstance(origin_obj, GangMember):
            fac = getattr(origin_obj, "faction", None)

            if fac:
                # Check if faction is a Gang object
                if getattr(fac, "type", None) == "gang":
                    if getattr(fac, "is_street_gang", False):
                        info = f"{fac.name} (street gang)"
                    else:
                        info = f"{fac.name} (gang)"
                else:
                    info = "GangMember (unknown faction)"
            else:
                info = "GangMember (unaffiliated)"
        # Furniture
        elif hasattr(origin_obj, "seating_capacity"):
            if origin_obj.occupants:
                info = f"{len(origin_obj.occupants)}/{origin_obj.seating_capacity} seated"
            else:
                info = f"{origin_obj.seating_capacity} seats"


        if hasattr(origin_obj, "modulated_ambience"):
            ambience = origin_obj.modulated_ambience()
            if ambience:
                top = max(ambience.items(), key=lambda x: x[1])
                info = f"Enhances {top[0]} (via {source})"
                #should the following code remain or be commented out?
                source = v.get("source")
                if source:
                    info = f"Enhances {top[0]} (via {source})"
                else:
                    info = f"Enhances {top[0]} (via UNKNOWN)"


        # Append row
        table_data.append([
            i,
            desc,
            type_,
            appearance,
            info,
        ])