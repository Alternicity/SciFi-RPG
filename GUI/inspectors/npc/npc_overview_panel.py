#GUI.inspectors.npc_overview_panel.py


from tkinter import ttk


def build_overview_panel(gui, parent):

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


        #wrong
        #getattr(npc.current_destination, "name", "-")

        gui.overview_labels[field] = value



def refresh_overview_panel(gui):

    npc = gui.selected_npc

    if not npc:
        return

    motivation_manager = getattr(npc, "motivation_manager", None)

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

    gui.overview_labels["Top Motivation"].config(
        text=top_text
    )

    gui.overview_labels["Name"].config(
        text=npc.name
    )

    gui.overview_labels["Debug Role"].config(
        text=getattr(npc, "debug_role", "-")
    )

    location_name = getattr(
        getattr(npc, "location", None),
        "name",
        "-"
    )

    gui.overview_labels["Location"].config(
        text=location_name
    )

    gui.overview_labels["Hunger"].config(
        text=str(getattr(npc, "hunger", "-"))
    )

    gui.overview_labels["Fun"].config(
        text=str(getattr(npc, "fun", "-"))
    )
    #added
    gui.overview_labels["Effort"].config(
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

    gui.overview_labels["Destination"].config(
        text=destination_name
    )

    #destination  missing here