#GUI.inspectors.entity.npc_inspector.py
from status import get_primary_status_display
from tkinter import ttk

def build_npc_inspector(gui, parent, npc):
    print("BUILD NPC INSPECTOR:", npc.name)
    
    for child in parent.winfo_children():
        child.destroy()

    ttk.Label(
        parent,
        text=npc.name
    ).pack(anchor="w", padx=10, pady=5)

    #defensive:
    role_text = getattr(
        npc,
        "debug_role",
        "Unknown"
    )

    ttk.Label(
        parent,
        text=f"Role: {role_text}"
    ).pack(anchor="w", padx=10)
    """ Later this probably becomes:
    npc.access_component """

    appearance = npc.appearance

    ttk.Label(
        parent,
        text=f"Race: {appearance['race']}"
    ).pack(anchor="w", padx=10)

    ttk.Label(
        parent,
        text=f"Sex: {appearance['sex']}"
    ).pack(anchor="w", padx=10)

    if npc.is_scenario_npc:

        ttk.Label(
            parent,
            text="Scenario NPC"
        ).pack(anchor="w", padx=10)

    if appearance.get("overall_impression"):
        pass#ATTN

    if appearance.get("is_visibly_wounded"):
        pass#ATTN

    if appearance.get("bloodstained"):
        pass#ATTN

    status_text = get_primary_status_display(npc)

    ttk.Label(
        parent,
        text=f"Status: {status_text}"
    ).pack(anchor="w", padx=10)

    access = getattr(
        npc,
        "access_component",
        None
    )

    if access:
        ttk.Label(
            parent,
            text=f"Access: {access}"
        ).pack(anchor="w", padx=10)

    

