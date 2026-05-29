#employment.employment_helpers.py

def is_employed(npc):
        return (
            hasattr(npc, "employment")
            and npc.employment is not None
            and npc.employment.workplace is not None
        )