#Luna_meta_tools.py
from character_memory import Memory
from memory_entry import MemoryEntry
from incompressible import Incompressible

def integrate_incompressible(memory: Memory, incompressible: Incompressible):
    entry = MemoryEntry(
        subject="Luna",
        object_=incompressible.symbol,
        verb="encountered",
        details=incompressible.reason,
        tags=["incompressible"] + (incompressible.tags or []),
        description="Encountered a symbol that resists collapse",
        payload=incompressible,
        type="anomaly",
        function_reference=None,
        implementation_path=None,
        associated_function=None
    )
    #memory.add_semantic(entry, category="incompressibles")
    #not currently seeded to Luna at instantiation