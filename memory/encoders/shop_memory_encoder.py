#memory.encoders.shop_memory_encoders.py
from base.core_types import KnowledgeBase
from memory.memory_entry import MemoryEntry

def encode_shop_knowledge(kb: KnowledgeBase, npc):
    return MemoryEntry(
        subject=f"shops:{kb.region}",
        object_=None,
        type="shop_knowledge",
        details=f"Shops and food shops in region {kb.region}",
        data=kb,                    # KnowledgeBase stored here
        confidence=1.0,
        owner=npc,
    )
