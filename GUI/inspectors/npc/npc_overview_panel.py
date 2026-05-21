#GUI.inspectors.npc_overview_panel.py

from tkinter import ttk

def build_overview_panel(gui, parent):
    print("BUILD OVERVIEW PANEL")
    frame = ttk.LabelFrame(parent, text="Overview")
    frame.pack(#added
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )
    
    gui.overview_labels = {}

    fields = [
        "Name",
        "Debug Role",
        "Location",
        "Destination",
        "Faction",
        "Top Motivation",
        "Hunger",
        "Fun",
        "Effort"
    ]

    for field in fields:

        row = ttk.Frame(frame)
        row.pack(fill="x", padx=5, pady=2)

        ttk.Label(
            row,
            text=f"{field}:",
            width=20
        ).pack(side="left")

        value = ttk.Label(
            row,
            text="-",
            justify="left",
            anchor="w"
        )
        value.pack(side="left")

        gui.overview_labels[field] = {
            "row": row,
            "label": value
        }



def refresh_overview_panel(gui):

    npc = gui.active_context["npc"]

    if not npc:
        return

    print("OVERVIEW PANEL REFRESH")
    print(npc)

    motivation_manager = getattr(
        npc,
        "motivation_manager",
        None
    )

    top_text = "-"

    if motivation_manager:

        top_motives = motivation_manager.get_top_motivations(2)

        if top_motives:

            lines = []

            for motive in top_motives:

                lines.append(
                    f"{motive.type} ({int(motive.urgency)})"
                )

            top_text = "\n".join(lines)

    gui.overview_labels["Top Motivation"]["label"].config(
        text=top_text
    )

    gui.overview_labels["Name"]["label"].config(
        text=npc.name
    )
    
    print(
        "DEBUG ROLE CHECK:",
        npc.name,
        getattr(npc, "debug_role", None)
    )
    
    debug_role = getattr(npc, "debug_role", None)

    if not debug_role:
        debug_role = "-"

    gui.overview_labels["Debug Role"]["label"].config(
        text=debug_role
    )

    faction = getattr(npc, "faction", None)

    faction_name = getattr(
        faction,
        "name",
        "-"
    )

    faction_label = gui.overview_labels["Faction"]["label"]

    faction_label.config(
        text=faction_name
    )

    if faction:

        faction_label.config(
            foreground="cyan",
            cursor="hand2"
        )

        faction_label.bind(
            "<Button-1>",
            lambda e, f=faction: gui.open_faction(f)
        )

    else:

        faction_label.config(
            foreground="white",
            cursor=""
        )

    location_name = getattr(
        getattr(npc, "location", None),
        "name",
        "-"
    )

    gui.overview_labels["Location"]["label"].config(
        text=location_name
    )

    gui.overview_labels["Hunger"]["label"].config(
        text=str(getattr(npc, "hunger", "-"))
    )

    gui.overview_labels["Fun"]["label"].config(
        text=str(getattr(npc, "fun", "-"))
    )

    gui.overview_labels["Effort"]["label"].config(
        text=str(getattr(npc, "effort", "-"))
    )

    destination = getattr(
        npc,
        "current_destination",
        None
    )

    destination_name = getattr(
        destination,
        "name",
        "-"
    )

    gui.overview_labels["Destination"]["label"].config(
        text=destination_name
    )
