#motivation.motivation.py 
from status import StatusLevel
from debug_utils import debug_print
CORE_MOTIVES = {"eat", "sleep", "work", "have_fun"}
class Motivation:
    def __init__(self, type, urgency=1, target=None, status_type=None, source=None, persistent=False):
        self.type = type  #  "join_gang"
        self.urgency = float(urgency)  # is this optimal, or should it just be self.urgency = urgency?
        self.target = target  #  "e.g. Red Fangs"
        self.status_type = status_type  #  "criminal"
        self.source = source  #  memory, event, etc.
        self.persistent = persistent
        self.suppressed = False
        self.suppression_reason = None
        

    def unsuppress(self):
        self.suppressed = False
        self.suppression_reason = None


    def __repr__(self):
        desc = f"{self.type} (urgency {self.urgency})"
        if self.target:
            desc += f", target: {self.target}"
        if self.status_type:
            desc += f", status: {self.status_type}"
        return desc

    def to_dict(self):
        return {
            "type": self.type,
            "urgency": self.urgency,
            "target": self.target,
            "status_type": self.status_type,
            "source": self.source,
        }

    @property
    def tags(self):
        from motivation.motivation_presets import get_tags_for_motivation
        return get_tags_for_motivation(self.type)

    @classmethod
    def from_dict(cls, data):
        return cls(
            type=data["type"],
            urgency=data.get("urgency", 5),
            target=data.get("target"),
            status_type=data.get("status_type"),
            source=data.get("source"),
        )

VALID_MOTIVATIONS = {
        "earn_money": 5,
        "eat": 0,
        "sleep": 0,  # Increases with fatigue
        "shelter": 3,
        "have_fun": 2,
        "unwind": 2,
        "find_safety": 9,
        f"gain_{StatusLevel.LOW.value}": 4,
        f"gain_{StatusLevel.MID.value}": 5,
        f"gain_{StatusLevel.HIGH.value}": 6,
        f"gain_{StatusLevel.ELITE.value}": 7,
        "join_gang": 5,
        "join_faction": 5,
        "obtain_weapon": 5,
        "obtain_ranged_weapon": 5,
        "protect_vip": 5,
        "buy_object": 6,
        "steal_money": 4,
        "steal_object": 3,
        "rob": 3,
        "shakedown": 3, #shakeDown(character, location, targetResource) #extract value through implied threat
        "escape_danger": 8,  # Very urgent in dangerous situations
        "virtue_signal": 1,
        "find_partner": 3,
        "switch_partner": 2,#hypergamy exists here, see switchPartner(actor, target, currentPartner): Must be a perceived upgrade
        "seek_attention": 2,
        "seek_validation": 2,
        "offer_validation": 4,
        "influence": 4, #influence(actor, target): Change some other characters variables. See Charm() and create_psyop() and influece()
        "increase_popularity": 3, #see charm(actor, target):
        "decrease_hostilities": 4, #see reassureRivals(Boss, rivals): and offerTruce(Boss, rivals): but also offerFauxTruce(Boss, rivals):
        "sow_dissent": 4, #sowDissent(Character, rivals) #weaken a rival or enemy factions loyalities
        "patrol": 3, #patrol(character, region, targetObjects) A key FSM action for low level faction members
        "snitch": 2, #snitch(character, target, location) If a character sees a crime, or feels threatened by faction behaviour
        "explore_math": 8,
        "use_advanced_python_features": 8,
        "stimulate_programmer": 8,
        "charm U7s": 20,
        "work": 12,
    }
    

class MotivationManager:
    def __init__(self, character):

        self.owner = character
        self.character = character#backwards compatibility
        
        self.motivations = []  #list of Motivation instances
        
        # optional global suppression bookkeeping
        self.suppressed = {}  
        # {motivation_type: reason}
        # example:
        # {
        #   "obtain_ranged_weapon": {
        #       "reason": "already_armed",
        #       "until": "inventory_change"
        #   }
        # }


    def set_urgency(self, type, value):
        """
        Set urgency for a motivation by type.
        If multiple exist, update all (safe default).
        """
        updated = False

        for m in self.motivations:
            if m.type == type:
                m.urgency = float(value)
                updated = True
        if type == "have_fun" and value <= 0:
            print(f"[DEBUG] have_fun dropped to {value}")

        matches = [m for m in self.motivations if m.type == type]#Is this ok here?

        if len(matches) > 1:
            print(f"[DUPLICATE MOTIVE] {type} count={len(matches)}")

        return updated

    def suppress(self, type, reason=None, duration=3):#line 134
        """
        Temporarily suppress a motivation for N ticks.
        """
        for m in self.motivations:
            if m.type == type:
                m.suppressed = True
                m.suppression_reason = reason
                m.suppression_timer = duration
                return m
        return None

    def consider_adding_motivation(
        self,
        mtype,
        urgency=1,
        target=None,
        source=None,
        status_type=None,
    ):
        npc = self.owner

        existing = self.get_motivation(mtype)

        # --- EXISTING: update ---
        if existing:
            if getattr(existing, "suppressed", False):
                return existing  # don't modify suppressed

            old = existing.urgency
            existing.urgency = max(existing.urgency, float(urgency))

            debug_print(
                npc,
                f"[MOTIVE] Updated {mtype} {old} → {existing.urgency} (source={source})",
                category="motive",
            )
            return existing

        # --- CREATE NEW ---
        motive = self._create_motivation(
            mtype, urgency, target, source, status_type
        )

        debug_print(
            npc,
            f"[MOTIVE] Added {mtype} (urgency={urgency}, source={source}, id={id(motive)})",
            category="motive",
        )

        return motive


        # --- CLEAR SUPPRESSION IF CONDITION NO LONGER HOLDS ---
        #became unreachable after the above code was updated
        """ if mtype in self.suppressed:
            del self.suppressed[mtype]#what is this doing? Will it run automatically

        # --- PASS THROUGH TO REAL ADD/UPDATE ---
        self.update_motivations(
            motivation_type=mtype,
            urgency=urgency,
            target=target,
            source=source,
            status_type=status_type,
        )
        return True """

    def get_top_motivation(self):
        return self.get_highest_priority_motivation()

    def debug_mind_state(npc):
        top_mot = npc.motivation_manager.get_top_motivation()
        top_thoughts = sorted(
            npc.mind.thoughts,
            key=lambda t: t.urgency,
            reverse=True
        )[:2]

        print(f"\n[MIND DEBUG] {npc.name}")

        if top_mot:
            print(f"  Motivation: {top_mot.type} ({top_mot.urgency})")

        print("  Thoughts:")
        for t in top_thoughts:
            print(f"    - {t.content} ({t.urgency})")

        anchor = npc.current_anchor.name if npc.current_anchor else "None"
        print(f"  Anchor: {anchor}")

    def unsuppress(self, type):
        for m in self.motivations:
            if m.type == type:
                m.suppressed = False
                m.suppression_reason = None
                m.suppression_timer = 0

    def update_suppressions(self):
        for m in self.motivations:
            if getattr(m, "suppressed", False):
                if not hasattr(m, "suppression_timer"):
                    continue

                m.suppression_timer -= 1

                if m.suppression_timer <= 0:
                    m.suppressed = False
                    m.suppression_reason = None
                    m.suppression_timer = 0

    # 🔹 MASTER SYNC — called once per tick
    def sync_motivations(self, tick):

        self.update_suppressions()
        self._debug_check("after update_suppressions")

        self.sync_physiological_motivations()
        self._debug_check("after sync_physiological")

        self.sync_role_motivations(tick)
        self._debug_check("after sync_role")  # 🔥 MOST IMPORTANT

        self.cleanup_suppressed()
        self._debug_check("after cleanup")

        self.deduplicate()
        
        if self.owner.debug_role in ("civilian_liberty", "civilian_worker", "civilian_waitress"):
            assert any(m.type == "have_fun" for m in self.motivations), \
                "have_fun vanished!"

        """ types = [m.type for m in self.motivations]#But the above assert already fired, so here there are no have_fun motivations?

        dupes = [t for t in set(types) if types.count(t) > 1]

        if dupes:
            print(f"[DUPLICATES DETECTED] {dupes}")
            print([
                (id(m), m.type, m.urgency, m.persistent)
                for m in self.motivations
                if m.type in dupes
            ]) """
            
    #TMP, I hope
    def _debug_check(self, stage):
        types = [m.type for m in self.motivations]

        if "have_fun" not in types:
            print(f"[MISSING have_fun] at {stage}")
            print([
                (id(m), m.type, m.urgency, m.persistent)
                for m in self.motivations
            ])

        dupes = [t for t in set(types) if types.count(t) > 1]

        if dupes:
            print(f"[DUPLICATES DETECTED at {stage}] {dupes}")
            print([
                (id(m), m.type, m.urgency, m.persistent)
                for m in self.motivations
                if m.type in dupes
            ])


    # 🔹 PHYSIOLOGY
    def sync_physiological_motivations(self):
        npc = self.owner

        # Eat
        eat_motive = self.get_motivation("eat")
        if eat_motive and eat_motive.suppressed:
            return  # 🔥 HARD BLOCK

        if npc.hunger >= 8 and not self.is_suppressed("eat"):
            self.consider_adding_motivation(
                "eat",
                urgency=npc.hunger,
                source="physiology"
            )
        # Sleep — rises as effort decays
        effort = getattr(npc, "effort", 10)
        if effort <= 6 and not self.is_suppressed("sleep"):
            sleep_urgency = max(1, round((10 - effort) * 1.2))
            self.consider_adding_motivation("sleep", urgency=sleep_urgency, source="physiology")
            debug_print(npc, f"[PHYSIO] sleep urgency={sleep_urgency} effort={effort:.1f}", 
                        category="motive")
        
    # 🔹 ROLE / OBLIGATION
    def sync_role_motivations(self, tick):
        npc = self.owner

        """ debug_print(
            self.owner,
            f"[ROLE SYNC START] {[(id(m), m.type, m.urgency, m.persistent) for m in self.motivations]}",
            category="motive"
        ) """

        on_shift = npc.is_on_shift  # use unified state

        if on_shift:
            self.unsuppress("work")

            BLOCKED_DURING_WORK = {"have_fun", "sleep", "eat"}#This could be all motivations except work. Also:
            """ eat removed from here, because it drives movement
            it creates anchors
            it prevents deadlock """

            for m in self.motivations:
                if m.type in BLOCKED_DURING_WORK:
                    self.suppress(m.type, reason="working")

        else:
            self.suppress("work", reason="off_shift", duration=999)

            # 🔥 release all others
            for m in self.motivations:
                if m.type != "work":
                    self.unsuppress(m.type)

        """ debug_print(
            self.owner,
            f"[ROLE SYNC END] {[(id(m), m.type, m.urgency, m.persistent) for m in self.motivations]}",
            category="motive"
        ) """
    #tmp?
    @property
    def urgency(self):
        return self._urgency

    @urgency.setter
    def urgency(self, value):
        if self.type == "have_fun":
            import traceback
            print(f"[DEBUG SET] have_fun → {value}")
            traceback.print_stack(limit=5)
        self._urgency = value

    def unsuppress(self, type):#See also the unsupress in class Motivation
        for m in self.motivations:
            if m.type == type:
                m.unsuppress()
                """ API is now:
                self.suppress("XYZ")
                self.unsuppress("XYZ") """

    def cleanup_suppressed(self):
        """ debug_print(
            self.owner,
            f"[MOTIVES BEFORE CLEANUP] {self.owner.name} {[(id(m), m.type, m.urgency, m.persistent) for m in self.motivations]}",
            category="motive"
        ) """

        kept = []
        removed = []

        for m in self.motivations:
            if m.persistent or m.urgency > 0 or getattr(m, "suppression_timer", 0) > 0:
                kept.append(m)
            else:
                removed.append(m)

        if removed:
            debug_print(
                self.owner,
                f"[MOTIVE CLEANUP] {self.owner.name} removed={[(m.type, m.urgency) for m in removed]}",
                category="motive"
            )

        self.motivations = kept

        """ debug_print(
            self.owner,
            f"[MOTIVES AFTER CLEANUP] {self.owner.name} {[(id(m), m.type, m.urgency, m.persistent) for m in self.motivations]}",
            category="motive"
        ) """




    #  A — INPUT COERCION HELPERS

    def _coerce_motivation_type(self, motivation_type) -> str:
        aliases = {
            "earn_money": "work",
        }

        if isinstance(motivation_type, str):
            return aliases.get(motivation_type, motivation_type)

        if hasattr(motivation_type, "type"):
            return aliases.get(motivation_type.type, motivation_type.type)

        if hasattr(motivation_type, "content"):
            return aliases.get(motivation_type.content, motivation_type.content)

        return str(motivation_type)

    #  B — MOTIVATION CREATION / GETTERS

    def add(self, motivation: Motivation):
        self.motivations.append(motivation)
        return motivation
    
    def is_suppressed(self, mtype):
        m = self.get_motivation(mtype)
        if not m:
            return False
        return getattr(m, "suppressed", False)
    
    def _create_motivation(self, mtype, urgency, target, source, status_type, persistent=False):
        existing = self.get_motivation(mtype)

        if existing:
            # Merge instead of duplicate
            existing.urgency = max(existing.urgency, float(urgency))
            existing.persistent = existing.persistent or persistent

            if target is not None:
                existing.target = target
            if source is not None:
                existing.source = source
            if status_type is not None:
                existing.status_type = status_type

            return existing

        new = Motivation(
            type=mtype,
            urgency=float(urgency),
            target=target,
            source=source,
            status_type=status_type,
            persistent=persistent
        )

        self.motivations.append(new)
        return new
    
    def create_initial(self, mtype, urgency=1, target=None, source="initial", status_type=None):
        """
        Legacy initializer used during character creation.
        Bypasses update logic and creates motivations directly.
        """
        #When upgrading see: motivation_presets.py for non test case npcs

        """ Right now you have two paths:
        create_initial() → direct creation
        update_motivations() → smart merge
        Long-term, you may want:
        create_initial → just call update_motivations """

        mtype = self._coerce_motivation_type(mtype)
        persistent = mtype in CORE_MOTIVES

        return self._create_motivation(
            mtype=mtype,
            urgency=urgency,
            target=target,
            source=source,
            status_type=status_type,
            persistent=persistent
        )

    def deduplicate(self):
        seen = {}
        for m in self.motivations:
            if m.type not in seen:
                seen[m.type] = m
            else:
                existing = seen[m.type]
                existing.urgency = max(existing.urgency, m.urgency)
                existing.persistent = existing.persistent or m.persistent

        self.motivations = list(seen.values())

    """def _create_motivation(self, mtype, urgency, target, source, status_type):

        new = Motivation(
            type=mtype,
            urgency=float(urgency),
            target=target,
            source=source,
            status_type=status_type
        )
        self.motivations.append(new)
        if mtype == "have_fun":#motivation was marked as not defined here, so I changed it to mtype
            print(f"[CREATE] from _create_motivation have_fun id={id(mtype)} persistent={mtype.persistent}")
        return new """

    def get_motivation(self, motivation_type):
        """Return the Motivation object matching this type name."""
        mtype = self._coerce_motivation_type(motivation_type)
        for m in self.motivations:
            if m.type == mtype:
                return m
        return None
    
    #  C — ADDING / UPDATING MOTIVATIONS

    def update_motivations(self, motivation_type, urgency=1, target=None, source=None, status_type=None):
        """
        Create or update a motivation.
        If it already exists:
          - urgency = max(existing.urgency, new urgency)
          - update target/source/status if provided
        """

        mtype = self._coerce_motivation_type(motivation_type)
        persistent = mtype in CORE_MOTIVES

        existing = self.get_motivation(mtype)

        if existing:
            existing.urgency = max(existing.urgency, float(urgency))
            if target is not None: existing.target = target
            if source is not None: existing.source = source
            if status_type is not None: existing.status_type = status_type
            return existing

        return self._create_motivation(mtype, urgency, target, source, status_type, persistent)

    def set_motivations(self, motivations_list):
        """Replace all existing motivations with a new list."""
        self.motivations = []
        for mtype, urgency in motivations_list:
            self.update_motivations(mtype, urgency)


    # user-friendly API aliases
    def increment(self, motivation_type, amount=1):
        return self.update_motivations(motivation_type, urgency=amount)

    def boost(self, motivation_type, amount):
        m = self.update_motivations(motivation_type, urgency=0)
        m.urgency += amount
        return m



    #  D — REMOVAL / CLEARING


    def remove_motivation(self, motivation_type):
        """Remove motivations of a given type. Return True if anything removed."""
        mtype = self._coerce_motivation_type(motivation_type)
        before = len(self.motivations)
        self.motivations = [m for m in self.motivations if m.type != mtype]
        return len(self.motivations) != before

    def resolve_motivation(self, type_name):
        """Alias for removal, clearer in some contexts."""
        self.motivations = [m for m in self.motivations if m.type != type_name]

    def clear_highest_priority_motivation(self):#not yet adapted to permanent motivations
        
        top = self.get_highest_priority_motivation()
        if top:
            self.motivations.remove(top)
        return top

    #  E — QUERIES / SORTING

    def get_highest_priority_motivation(self, exclude=None):
        exclude = exclude or set()

        valid = [
            m for m in self.motivations
            if m.type not in exclude and not m.suppressed
        ]

        if not valid:
            return None

        return max(valid, key=lambda m: m.urgency)

    def get_top_motivations(self, n=2, include_zero=False):
        """
        Return the top-N motivations sorted by urgency (descending).
        """
        motivations = list(self.motivations)

        if not motivations:
            return []

        if not include_zero:
            motivations = [m for m in motivations if getattr(m, "urgency", 0) > 0]

        motivations.sort(key=lambda m: getattr(m, "urgency", 0), reverse=True)

        return motivations[:n]

    def get_motivations(self):
        """Return all motivations sorted by urgency."""
        return sorted(self.motivations, key=lambda m: m.urgency, reverse=True)

    def sorted_by_urgency(self, descending=True):
        return sorted(self.motivations, key=lambda m: m.urgency, reverse=descending)

    def get_urgent_motivations(self, threshold=7):
        return [m for m in self.motivations if m.urgency >= threshold]

    def has(self, motivation_type):
        """Alias for has_motivation()"""
        return any(m.type == motivation_type for m in self.motivations)

    def has_motivation(self, motivation_type):
        """Return True if a motivation with this type exists."""
        return self.has(motivation_type)

    def get_urgency(self, motivation_type):
        for m in self.motivations:
            if m.type == motivation_type:
                return m.urgency
        return 0

    def deboost_others(self, except_type: str, amount: float = 3):
        """
        Reduce urgency of all motivations except the specified type.
        Prevents going below zero.
        """
        for m in self.motivations:
            if m.type != except_type:
                m.urgency = max(0.1, m.urgency - amount)
                #the 0.1 is a clamp, preventing negative numbers, or zero

    #  F — DEBUG / DISPLAY

    def get_motivations_display(self):
        """Return simple strings suitable for debug output."""
        return [f"{m.type} (urgency {m.urgency:.1f})" for m in self.motivations]
    
    

class PoeticMotivation(Motivation):
    metaphor: str
    #You could later generate quests based on poetic triggers


#Utility Functions
def debug_motivations(npc, top=3):

        mm = npc.motivation_manager
        motivations = mm.sorted_by_urgency()

        lines = [
            f"{m.type}:{m.urgency:.1f}"
            for m in motivations[:top]
        ]

        debug_print(
            npc,
            "[MOTIVATIONS] " + ", ".join(lines),
            category="motivation"
        )