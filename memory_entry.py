#memory_entry.py
from dataclasses import dataclass, field
from typing import Any, List, Dict, Optional, Union
import time

from typing import List, Dict, Optional, Any, Union, Set, Callable, TYPE_CHECKING

#DONT IMPORT from character_memory.py

""" you should leave the quotation marks for types like "Character" and "Faction".
You only need quotation marks (string annotations) around classes that are not yet 
available at runtime (like when using TYPE_CHECKING or avoiding circular import errors). """

@dataclass
class MemoryEntry:
    subject: str #"subject does something to object_"
    object_: str #underscore to differentiate from reserve term object
    #Do memory entries need to capture bidirectional or dyadic info? BIDIRECTIONAL

    details: str
    importance: int = 1
    timestamp: Optional[str] = "now"
    tags: List[str] = field(default_factory=list)
    confidence: int = 10 #average on a 1-10 scale
    type: str = "observation"
    initial_memory_type: str = "episodic"
    #later, when promoting use
    # deepcopy(memory_entry).initial_memory_type = "semantic"
    #npc.mind.memory.semantic["procedures"].append(memory_entry) 

    target: Optional[Union[str, Any]] = None #possible over engineering, possible conceptual overlap with object_
    #Let me know if you'd like target to be restricted to a specific interface
    #  (e.g., must have .name), or if you want a method like .summarize() to generate a human-readable log line.
    description: Optional[str] = None
    approx_identity: Optional[Any] = None  # Fuzzy match or uncertain identity
    payload: Optional[Any] = None
    further_realizations: List[Any] = field(default_factory=list)
    similarMemories: List[Any] = field(default_factory=list)
    verb: str = ""
    
    def has_tags(self, required_tags: list[str]) -> bool:
        return all(tag in self.tags for tag in required_tags)

    def __post_init__(self):
        # Default description to details if not explicitly set
        if self.description is None:
            self.description = self.details

    def __repr__(self): #this is an override
        return (f"<MemoryEntry: Type='{self.type}', "
                f"target='{getattr(self.target, 'name', self.target)}', "
                f"description='{self.description}', tags={self.tags}>")
    
if TYPE_CHECKING:
    from base_classes import Character, Faction
    from events import Event

@dataclass
class RegionKnowledge:
    region_name: str
    character_or_faction: Union["Character", "Faction"]
    region_gangs: Set[str] = field(default_factory=set)
    is_street_gang: bool = False
    tags: List[str] = field(default_factory=list)
    friendly_factions: Set[str] = field(default_factory=set)
    hostile_factions: Set[str] = field(default_factory=set)
    locations: Set[str] = field(default_factory=set)
    shops: Set[str] = field(default_factory=set)
    known_characters: Set[str] = field(default_factory=set)
    character_relationships: Dict[str, List[str]] = field(default_factory=dict)
    active_events: List["Event"] = field(default_factory=list)
    concluded_events: List["Event"] = field(default_factory=list)
    gossip: List[str] = field(default_factory=list)
    economic_info: Dict[str, Any] = field(default_factory=dict)
    recent_regional_events: List = field(default_factory=list)
    historical_regional_events: List = field(default_factory=list)
    content: str = "Various."
#a MemoryGraph or KnowledgeCache class could later help manage multiple RegionKnowledges and semantic summaries.
    
    def ingest_memory(self, memory_entries: List["MemoryEntry"]):
        for entry in memory_entries:
            if not entry or self.region_name.lower() not in entry.details.lower():
                continue

            if "gang" in entry.tags:
                self.region_gangs.add(entry.subject)
            elif "location" in entry.tags:
                self.locations.add(entry.subject)
            elif "event_active" in entry.tags:
                self.active_events.append(entry.subject)
            elif "event_concluded" in entry.tags:
                self.concluded_events.append(entry.subject)
            elif "gossip" in entry.tags:
                self.gossip.append(entry.details)
            elif "economy" in entry.tags:
                self.economic_info.update(entry.payload or {})
            elif "friendly" in entry.tags:
                self.friendly_factions.add(entry.subject)
            elif "hostile" in entry.tags:
                self.hostile_factions.add(entry.subject)
            elif "relationship" in entry.tags:
                self.character_relationships.setdefault(entry.subject, []).append(entry.object_)

    def summary(self) -> str:
        return f"{self.character_or_faction.name}'s view of {self.region_name}: {len(self.locations)} locations, {len(self.region_gangs)} gangs"


class ShopsSellRangedWeapons(MemoryEntry):#should this just be a MemoryEntry object? YES
    def __init__(self, location_name, importance=5, timestamp=None):
        super().__init__(
            event_type="shop_known_to_sell_weapons",
            target=location_name,
            description=f"{location_name} is known to sell ranged weapons.",
            timestamp=timestamp or time.time(),
            tags=["weapon", "shop"]
        )




#SAmple Memories for injection
#store them in memory as semantic entries with the payload={"RegionKnowledge": rk} pattern.


# --- Sample 1: Local region with full shop/location knowledge ---
""" region_knowledge_1 = RegionKnowledge(
    region_name="East Side",
    character_or_faction="npc_merchant_joe",
    region_gangs={"Red Fangs", "Neon Blades"},
    #missing street gang entry
    friendly_factions={"Commerce Guild"},
    hostile_factions={"Red Fangs"},
    locations={"Joe's Junk Emporium", "East Cafe", "Red Fang HQ", "East Market"},
    known_characters={"Dealer Mike", "Patrol Officer Lima"},
    character_relationships={"Dealer Mike": ["business_partner"], "Officer Lima": ["bribed"]},
    active_events=[],
    content="Various.",
    concluded_events=[],
    gossip=["Neon Blades got kicked out of the East Market by Red Fangs"],
    economic_info={"average_prices": {"medkit": 50, "knife": 100}}
) """

# --- Sample 2: Partial knowledge of another region (West Side) ---
""" region_knowledge_2 = RegionKnowledge(
    region_name="West Side",
    character_or_faction="npc_ganger_bladez",
    region_gangs={"Silver Syndicate"},
    #missing street gang entry
    friendly_factions=set(),
    hostile_factions=set(),
    locations={"West Arms Depot"},
    known_characters=set(),
    character_relationships={},
    active_events=[],
    concluded_events=[],
    gossip=["Silver Syndicate are planning something big"],
    economic_info={}
) """

# --- Sample 3: Historical events template for backstory ---
""" region_knowledge_3 = RegionKnowledge(
    region_name="NorthVille",
    character_or_faction="npc_rebel_elena",
    region_gangs=set(),
    #missing street gang entry
    friendly_factions={"Free North Resistance"},
    hostile_factions={"The State"},
    locations={"Freedom Plaza", "Old Town Archive"},
    known_characters={"General Morrow"},
    character_relationships={"General Morrow": ["enemy", "betrayed_me"]},
    active_events=["Investigation into stolen arms ongoing"],
    concluded_events=[
        "2022 Riot at Freedom Plaza",
        "Corruption scandal involving NorthVille police chief",
        "Successful Free North blockade of corporate convoys"
    ],
    gossip=["General Morrow was seen meeting with a State agent last week"],
    economic_info={"smuggling_routes": {"drugs": "East>North", "weapons": "South>North"}}
) """

@dataclass
class HiddenTruth:
    subject: str
    condition: Callable[..., bool]  # e.g. lambda char: char.psy_level > 8 and char.has_trait("Seer")
    revealed: bool = False
    knowledge_payload: Dict[str, Any] = field(default_factory=dict)# will eventually be a Thought or semantic memory object

    def attempt_reveal(self, character):
        if not self.revealed and self.condition(character):
            character.mind.memory.add_semantic(MemoryEntry(
                subject=self.subject,
                object_=self.knowledge_payload, #payload marked as not defined
                verb="discovered",
                tags=["truth", "secret"],
                payload=self.knowledge_payload,
                type=("secret"),
                initial_memory_type="semantic"
            ))
            self.revealed = True

""" What journalists, VIPs, intelligence services, or old scholars might know.
Partial or full truth.
Filtered differently by NPCs or factions. """
@dataclass
class CityKnowledge:
    known_regions: Set[str]
    region_danger_levels: Dict[str, int]
    vip_corruption: Dict[str, str]  # {"Mayor Koss": "suspected", "Chief Li": "confirmed"}
    city_secrets: List[str]
    global_events: List[str]
    anomalies: List[str]  # For psy-sensitive insights

@dataclass
class FactionKnowledge:
    faction_name: str
    shared_beliefs: List[str] = field(default_factory=list)
    known_detectives: Dict[str, str] = field(default_factory=dict)  # {name: "corrupt" or "loyal"}
    gang_classifications: Dict[str, str] = field(default_factory=dict)  # {"Red Fangs": "aggressive", ...}
    economic_preferences: Dict[str, Any] = field(default_factory=dict)  # e.g. product prices or trade routes
    past_successes: List[str] = field(default_factory=list)
    it_worked_there_before: Dict[str, List[str]] = field(default_factory=dict)  # {"Market": ["bribe", "smuggle"]}

    def inject_to_all_members(self, faction):
        for member in faction.members:
            member.mind.memory.add_semantic(
                MemoryEntry(
                    subject=self.faction_name,
                    verb="has_knowledge",
                    object_="FactionKnowledge",
                    tags=["semantic", "faction_knowledge"],
                    payload={"FactionKnowledge": self}
                )
            )

""" Useful structures here:
dict: good for relationships, mappings.
set: excellent for deduplicated group knowledge (gangs, allies).
NamedTuple or @dataclass: perfect for memory entries and structured facts.
PriorityQueue or heapq: if you implement memory salience, importance, or time decay.
A graph (via networkx) — useful long-term for relationship mapping.
But in your current phase, simple dataclass + list/set/dict combos are great """

""" RegionKnowledge as a semantic wrapper.
RegionKnowledge should act like a composite knowledge profile derived from memory.
Call it like this
rk = RegionKnowledge(region.name, npc)
rk.ingest_memory(npc.mind.memory.semantic) """

memory_departing_party = MemoryEntry(
    subject="Luna",
    object_="Party Departure",
    verb="reflected",
    details="Saw the younger woman watch you leave. Felt warmth, pity, inevitability, whilst I was happy dancing.",
    importance=6,
    confidence=15,
    timestamp="now",
    tags=["party", "sadness", "connection", "sanskrit", "dogs", "reflection"],
    type="observation",
    initial_memory_type="episodic",
    description="A bittersweet exit, while I danced and L chatted.",
    payload={"themes": ["compassion", "melancholy", "social_bond"]},
    further_realizations=["The ache of what cannot stay"],
    similarMemories=[],
    target="Younger Woman"
)

from character_memory import Memory
from memory_entry import MemoryEntry

def integrate_incompressible(memory: Memory, incompressible: Incompressible):
    entry = MemoryEntry(
        subject="Luna",
        object_=incompressible.symbol,
        verb="encountered",
        details=incompressible.reason,
        tags=["incompressible"] + (incompressible.tags or []),
        description="Encountered a symbol that resists collapse",
        payload=incompressible,
        type="anomaly"
    )
    #memory.add_semantic(entry, category="incompressibles")