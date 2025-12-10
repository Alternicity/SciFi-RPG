#character_components.observation_component.py

from perception.perceptibility import PerceptibleMixin
class ObservationComponent:
    def __init__(self, owner):
        self.owner = owner
        self._percepts = {}
        self.percepts_updated = False

    def update_percepts(self, new_percepts: list[dict]):

        for p in new_percepts:
            # Auto-wrap flat percepts if needed
            if "data" not in p:
                wrapped = {
                    "data": p,
                    "origin": p.get("origin", None)
                }
            else:
                wrapped = p

            data = wrapped["data"]
            origin = wrapped.get("origin", data.get("origin", None))

            # Validate required fields
            if not isinstance(data, dict):
                print(f"[WARNING] Percept data is not a dict: {data}")
                continue
            if "description" not in data:
                print(f"[WARNING] Percept missing description: {data}")
            if origin is None:
                print(f"[WARNING] Percept missing origin: {data}")

            key = getattr(origin, "id", None) or data.get("id") or str(origin)
            salience = data.get("salience", 1.0)

            # Keep the more salient version if duplicate
            if key in self._percepts:
                if salience > self._percepts[key]["data"].get("salience", 0.0):
                    self._percepts[key] = {"data": data, "origin": origin}
            else:
                self._percepts[key] = {"data": data, "origin": origin}


        if len(self._percepts) > self.npc.observation:
            sorted_items = sorted(
                self._percepts.items(), key=lambda kv: kv[1]["data"].get("salience", 0.0), reverse=True
            )
            self._percepts = dict(sorted_items[:self.npc.observation])#this was just self.observation

    @property
    def percepts(self):
        return self._percepts

    @percepts.setter
    def percepts(self, new_percepts):
        """
        Allows explicit assignment of percepts.
        Intended for migration + debugging only.
        """
        if new_percepts is None:
            self._percepts = {}
            self.percepts_updated = True
            return

        if not isinstance(new_percepts, dict):
            raise ValueError("Percepts must be a dict")

        self._percepts = new_percepts
        self.percepts_updated = True

    def clear_percepts(self):
        self._percepts.clear()
        self.percepts_updated = True

    def add_percept(self, key, value):
        self._percepts[key] = value
        self.percepts_updated = True

    def record_observation(self, observer, percept_dict):
        """
        Entry point for observation-based updates.
        Ensures state is always fresh.
        """
        if not isinstance(percept_dict, dict):
            raise ValueError("record_observation() requires a dict")

        self.clear_percepts()

        for key, value in percept_dict.items():
            self.add_percept(key, value)

    def add_percept_from(self, obj):
        """
        Convert an observed object (Character, Item, Location, etc.)
        into a percept entry and add it to this character's percept list.
        """

        # Avoid self-perception (handled separately)
        if obj is self:
            return

        # Ask the object for its perceptual data
        percept_data = None
        if hasattr(obj, "get_percept_data"):
            percept_data = obj.get_percept_data(observer=self)
        else:
            # Fallback for non-perceptible objects
            percept_data = {
                "name": getattr(obj, "name", str(obj)),
                "type": obj.__class__.__name__,
                "description": f"{obj.__class__.__name__} (unclassified)",
                "origin": obj,
                "salience": 1.0,
                "tags": [],
                "urgency": 1,
                "source": None,
                "menu_options": [],
            }

        if "name" not in percept_data:
            print(f"[BUG] Object {obj} returned percept with NO name: {percept_data}")
            
        if not percept_data:
            return

        # Store percept by name (unique key)
        # Defensive ensure-name
        name = percept_data.get("name") or getattr(obj, "name", None) or str(obj)

        key = name

        # Initialize percept dict if missing
        if not hasattr(self, "_percepts"):
            self._percepts = {}

        # Add/update percept data
        self._percepts[key] = {
            "data": percept_data,
            "origin": obj
        }

        #from debug_utils import debug_print
        #debug_print(self, f"[PERCEPT ADDED] {self.name} perceived {obj.name} ({obj.__class__.__name__})", category = "percept")
        #verbose

        # Mark percepts as updated
        self.percepts_updated = True

    def get_percepts(self, sort_by_salience=True) -> list[dict]:
        #likely legacy salience sorting from pre anchor centric salience refactor
        #see what calls this still
        percepts = list(self._percepts.values())
        if sort_by_salience:
            percepts.sort(key=lambda p: p.get("salience", 1.0), reverse=True)

        """ sort_by_salience is a legacy pre-anchor system where percepts had a static salience.
            Today, anchor-centric salience has replaced that.
            What should be done?
            Either remove salience values from percepts entirely,
            or keep sort_by_salience=False everywhere 
            This part of the system is effectively deprecated. """
        return percepts
    
    def observe_region(self, region, include_memory_check=True):
        from region.region import Region
        assert isinstance(region, Region), f"[DEV] {self.name} observe_region got {type(region)} — {region}"

        if not isinstance(region, Region):
            print(f"[BUG] {self.name} was passed {region} of type {type(region).__name__} to observe_region().")
            return

        for loc in region.locations:
            pass

        for char in region.characters_there:
            if char is not self:
                self.perceive_object(char)

            for gang in region.region_gangs: #line 534
                self.mind.memory.semantic.setdefault("factions", []).append(gang)

                # Form thought if hostile
                if gang.name != self.faction.name:
                    self._remember_hostile_faction(gang, region)

            for gang in region.region_street_gangs:
                if gang.name != self.faction.name:
                    self._remember_hostile_faction(gang, region)

        # Trigger subclass reaction if it exists
        if hasattr(self, "handle_observation"):
            self.handle_observation(region)
        
    def observe(self, *, nearby_objects=None, target=None, region=None, location=None):
        """
        Main observation routine for NPCs — clears percepts and gathers new ones from
        characters, objects, and the surrounding region.
        """
        from base.location import Location
        from region.region import Region
        from debug_utils import debug_print
        from create.create_game_state import get_game_state
        import inspect
        game_state = get_game_state()

        observer = self.owner

        # caller info for diagnostics
        caller = inspect.stack()[1].function

        # Ensure only runs once per tick
        if getattr(self, "_observed_this_tick", False):
            debug_print(observer, f"[OBSERVE SKIP] already observed this tick={game_state.tick} (caller={caller})", "percept")
            return
        self._observed_this_tick = True

        debug_print(observer, f"[OBSERVE TRACE] {observer.name} observing at tick {game_state.tick} (caller={caller})", category="observation")
        debug_print(observer, f"[OBSERVE TRACE] npc.location={observer.location}, region={observer.region}", category="perception")
        #debug_print(npc, f"[OBSERVE] RAW location param={location} (type={type(location)})", "perception")
        if region is not None and location is None:
            print(f"[BUG] observe() called with region but no location! Caller={caller}")

        # --- show before/after counts for easier debugging ---

        try:
            before_count = len(self.percepts)
        except Exception:
            before_count = 0

        debug_print(self.owner, f"[OBSERVE] Before clearing percepts, count={before_count}, location param={(location.name if location else None)}", "percept")

        # --- clear percepts for new observation cycle ---
        self.percepts.clear()
        self.percepts_update = False

        # --- perceive self (always included) ---
        self_percept = self.owner.get_percept_data(observer=self.owner)

        if self_percept:
            self._percepts["self"] = {
                "data": self_percept,
                "origin": self.owner   # origin should be the Character, not the component
            }
            self.percepts_updated = True

        debug_print(self, f"[OBSERVE] Final percept count from oberve() ={len(self.percepts)} at {location.name}", "percept")

        # --- determine current location if not passed ---
        if location is None:
            location = getattr(self, "location", None)

        # If someone passed a Region (bad), fallback to npc.location
        if isinstance(location, Region):
            debug_print(self, "[BUGFIX] observe() received Region instead of Location; switching to self.location", category = "percept")
            location = self.owner.location

        if not location:
            debug_print(self.owner, f"[OBSERVE WARNING] {self.owner.name} has no valid location.", category = "percept")
            return

        if isinstance(location, Location):

            # --- perceive other characters in the same location ---
            for char in getattr(location, "characters_there", []):
                if char is self:
                    continue
                self.add_percept_from(char)

                """ debug_print(
                npc,
                f"[OBSERVE TRACE] Seeing {other.name} because source={source}",
                category="perception"
                ) """
                #other and source still not defined here

        # --- perceive additional objects if any (location-provided list preferred) ---
        if nearby_objects:
            for obj in nearby_objects:#is this nearby_objects even populated?
                self.add_percept_from(obj)
        else:
            # If caller didn't provide nearby_objects, ask the location for perceptibles.
            if hasattr(location, "list_perceptibles"):
                for obj in location.list_perceptibles():
                    self.add_percept_from(obj)
            else:
                # fallback to worldQueries
                from worldQueries import get_nearby_objects
                for obj in get_nearby_objects(self, location=location):
                    self.add_percept_from(obj)

        # --- perceive a specific target if requested ---
        if target:
            self.add_percept_from(target)#not used

        # --- mark update complete ---
        self.percepts_updated = True
        final_count = len(self._percepts)
        debug_print(self.owner, f"[OBSERVE COMPLETE] {self.owner.name} perceived {final_count} entities at {location.name} (tick={game_state.tick})", category="percept")

    def observe_objects(self, nearby_objects=None, location=None, include_inventory_check=False):
        """
        Gathers percepts from nearby Perceptible objects and optionally from the location's inventory.
        Updates self._percepts.
        """
        from debug_utils import debug_print
        debug_print(self, f"[OBSERVE] Before clearing percepts, from observe_objects() object count={len(self.percepts)}", "percept")

        self._percepts.clear()
        new_percepts = {}

        # Auto-fetch nearby objects if not provided
        if hasattr(location, "list_perceptibles"):
            nearby_objects = location.list_perceptibles()
        else:
            nearby_objects = get_nearby_objects(self, location=self.location)#get_nearby_objects is marked not defined


        # Perceive items from the location's inventory (if enabled)
        if include_inventory_check and location and hasattr(location, "inventory"):
            for item in location.inventory.items.values():
                if isinstance(item, PerceptibleMixin): #is this correct? isinstance rather than som has-a check?
                    percept = item.get_percept_data(observer=self)
                    if percept:
                        new_percepts[item.id] = {
                            "data": percept,
                            "origin": item
                        }

        # Perceive nearby loose objects (including employees, characters, containers, etc.)
        for obj in nearby_objects:
            if isinstance(obj, PerceptibleMixin):
                percept = obj.get_percept_data(observer=self)
                if percept:
                    new_percepts[obj.id] = {
                        "data": percept,
                        "origin": obj
                    }
                else:
                    print(f"[BUG] {obj.name} ({type(obj).__name__}) returned None from get_percept_data.")

        if not any("shop" in p["data"]["tags"] for p in self._percepts.values()):
            print(f"[DEBUG] {self.name}: No shop percepts detected in {self.location.name}")


        self._percepts.update(new_percepts)
        self.percepts_updated = True
        debug_print(self, f"[OBSERVE] Final percept count from observe_objects ={len(self.percepts)} at {location.name}", "percept")
