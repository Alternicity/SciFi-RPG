#GUI.inspectors.entity.npc_inspector.py
from status import get_primary_status_display
from tkinter import ttk
from GUI.viewmodels.character_inspector_display import get_character_inspector_data

def build_npc_inspector(gui, parent, npc, observer=None):
    print("BUILD NPC INSPECTOR:", npc.name)
    print("=== INSPECTOR OBSERVER ===", getattr(observer, "name", None))
    print("PARENT:", parent)


    vm = get_character_inspector_data(npc, observer=observer)

    for child in parent.winfo_children():
        child.destroy()

    ttk.Label(
        parent,
        text=vm.name
    ).pack(anchor="w", padx=10, pady=5)

    for section in vm.sections:
        ttk.Label(
            parent,
            text=f"{section.label}: {section.value}"
        ).pack(anchor="w", padx=10)

    print("=== BUILD NPC INSPECTOR COMPLETE ===", npc.name)
    print("  children now:", [type(c).__name__ for c in parent.winfo_children()])

""" def build_npc_inspector(gui, parent, npc, observer=None):
    print("BUILD NPC INSPECTOR:", npc.name)
    print("=== INSPECTOR OBSERVER ===", getattr(observer, "name", None))
    print("PARENT:", parent)
    print("CHILDREN BEFORE CLEAR:", [type(c).__name__ for c in parent.winfo_children()])

    percept = npc.get_percept_data(observer=observer)

    for child in parent.winfo_children():
        child.destroy()

    print("CHILDREN AFTER CLEAR:", [type(c).__name__ for c in parent.winfo_children()])

    ttk.Label(
        parent,
        text=npc.name
    ).pack(anchor="w", padx=10, pady=5)

    observable = percept.get("observable_traits", [])

    if observable:
        ttk.Label(
            parent,
            text="Observed: " + ", ".join(observable)
        ).pack(anchor="w", padx=10)

    if percept.get("race"):
        ttk.Label(parent, text=f"Race: {percept['race']}").pack(anchor="w", padx=10)

    if percept.get("sex"):
        ttk.Label(parent, text=f"Sex: {percept['sex']}").pack(anchor="w", padx=10)

    if percept.get("bloodstained"):
        blood = percept["bloodstained"]
        who = getattr(blood, "name", blood)
        ttk.Label(
            parent,
            text=f"Bloodstained ({who})"
        ).pack(anchor="w", padx=10)

    if percept.get("is_visibly_wounded"):
        ttk.Label(
            parent,
            text="Visibly wounded"
        ).pack(anchor="w", padx=10)

    if percept.get("posture") is not None:
        ttk.Label(
            parent,
            text=f"Posture: {percept['posture'].name.title()}"
        ).pack(anchor="w", padx=10)

    if percept.get("seated_at") is not None:
        ttk.Label(
            parent,
            text=f"Seated at: {percept['seated_at'].name}"
        ).pack(anchor="w", padx=10)

    for effect in npc.effects:
        symptoms = effect.visible_symptoms()
        if symptoms:
            ttk.Label(parent, text=f"Effect: {', '.join(symptoms)}").pack(anchor="w", padx=10)

    rel = observer.social_memory.relations.get(npc.id) if observer else None


    if rel:
        ttk.Label(parent, text=f"Relation: {rel.current_type}").pack(anchor="w", padx=10)
        # Only show scalars if familiarity is above some threshold
        if rel.familiarity >= 3:
            ttk.Label(parent, text=f"Trust: {rel.trust}  Familiarity: {rel.familiarity}").pack(anchor="w", padx=10)
            ttk.Label(parent, text=f"Affection: {rel.affection}  Fear: {rel.fear}").pack(anchor="w", padx=10)
        if rel.past_types:
            ttk.Label(parent, text=f"Previously: {', '.join(rel.past_types)}").pack(anchor="w", padx=10)
    else:
        ttk.Label(parent, text="Relation: unknown").pack(anchor="w", padx=10)

    status_text = get_primary_status_display(npc)

    ttk.Label(
        parent,
        text=f"Status: {status_text}"
    ).pack(anchor="w", padx=10)

    print("=== BUILD NPC INSPECTOR COMPLETE ===", npc.name)
    print("  children now:", [type(c).__name__ for c in parent.winfo_children()])

    access = getattr(
        npc,
        "access_component",
        None
    )

    if access:
        ttk.Label(
            parent,
            text=f"Access: {access}"
        ).pack(anchor="w", padx=10) """

    

