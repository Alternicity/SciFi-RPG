from dataclasses import field
import uuid
from distributions import generate_normal, generate_black_swan
from combat import calculate_intimidation_score, calculate_resistance_score
from characterActionTests import IntimidationTest
from InWorldObjects import ObjectInWorld
from visual_effects import loading_bar, RED, color_text
from abc import ABC, abstractmethod
from memory_entry import MemoryEntry

from output_utils import group_reactions


class Event(ABC):
    """ Do not make Event perceptible.
    Instead, Events cause percepts via the observe() system. """
    def __init__(self, name, event_type, effect=None, description="", impact=None, **kwargs):
        self.name = name
        self.event_type = event_type  # e.g., "normal", "black_swan", "incident", etc.
        self.effect = effect or {}    # e.g., {"impact": "modify", "attribute": "status"}
        self.description = description
        self.impact = impact or {}    # dict of actual changes to apply
        self.params = kwargs
        #effect gives structure, impact gives raw values. I think! Maybe consolidate?
        #Consider whether Event needs a timestamp or duration field

    @abstractmethod
    def resolve(self):
        pass

    def apply(self, character):
        # Generic application of event impact (expand this later)
        for attr, value in self.impact.items():
            if hasattr(character, attr):
                current = getattr(character, attr)
                setattr(character, attr, current + value)
                print(f"{character.name}'s {attr} increased by {value} (now {getattr(character, attr)})")
    
        
    """ @staticmethod
    def handle_incident(character, location=None):
        location = location or character.location  # fallback if None
        severity = 2  # or dynamic
        incident = Incident(name="Suspicious Activity", instigator=character, location=location, severity=severity)
        incident.resolve() """

    @staticmethod
    def get_character_driven_event_outcomes(character, location=None):
        return {
            "success": lambda: print(f"{character.name} successfully completes the action."),
            "detected": lambda: print(f"{character.name} was spotted! Guards are alerted."),
            "parsimony_opportunity": lambda: print(f"{character.name} notices another opportunity."),
            "triggered_trap": lambda: print(f"{character.name} sets off a trap! Trouble ahead."),
            "incident": lambda: Event.handle_incident(character, location)
 
            
        }
    @staticmethod
    def trigger_event_outcome(character, event_name, location=None):
        outcomes = Event.get_character_driven_event_outcomes(character, location)

        #get_character_driven_event_outcomes is marked as not defined
        outcomes.get(event_name, lambda: print(f"Unknown event outcome: {event_name}"))()

""" Possible Event types: Emergence, Fracture, Choice, Dream, Revelation
This could allow narrative-level motivation structures (beyond momentary urges). """

class TemplateEvent(Event):
    def __init__(self, instigator, location, **kwargs):
        super().__init__(
            name="Template Event",
            event_type="incident",  # e.g. "incident", "normal", etc.
            description="A template event. Customize this description.",
            impact={"fun": -1},  # Replace or remove as needed
            **kwargs
        )
        self.instigator = instigator
        self.location = location

    def resolve(self, simulate=False, verbose=True):
        if verbose:
            print(f"[Event]: {self.description}")

        # Apply the generic impact
        self.apply(self.instigator)

        # Create and distribute perceptual events if needed
        self.generate_percepts()

        # Optional: trigger outcome logic — useful if you decide to use it
        if hasattr(Event, "trigger_event_outcome"):
            Event.trigger_event_outcome(self.instigator, "incident", self.location)

        return self

    def generate_percepts(self):
        # Isolate percept logic from resolve()
        percept = {
            "description": f"{self.name} at {self.location.name}",
            "origin": self,
            "tags": ["template", "event"],
            "salience": 1.0,
            "location": self.location.name,
            "region": getattr(self.location, "region", "unknown"),
        }


        #note observer is also used in percept system
        observers = getattr(self.location, "list_characters", lambda exclude=None: [])(exclude=[self.instigator])
        for observer in observers:
            observer.perceive_event(percept)
            if hasattr(observer, "memory"):
                observer.memory.append(MemoryEntry(
                    subject="Shop",
                    object_="ranged_weapon",
                    details="Shops usually have weapons",
                    importance=6,
                    type="template_event_observed",
                    target=self.instigator,
                    approx_identity=self.instigator.get_appearance_description(),
                    description=f"Template Event Memory.",
                    initial_memory_type="episodic"
                ))

    def conclude(self):
        print(f"[DEBUG] {self.name} at {self.location.name} has concluded.")
        # Optional cleanup or progression logic here

class RandomEvent(Event):
    pass
    #environmental, market or mass formation psychosis events. The latter might spawn a temporary faction like object
        #or affect many characters motivations

class StateDrivenEvent(Event):
    def should_trigger(self, faction):
        return faction.morale < 20 or faction.revenge_meter > 5
    #We're here to help

class FactionDrivenEvent(Event):
    def should_trigger(self, faction):
        return faction.morale < 20 or faction.revenge_meter > 5
#A Boss or CEO decides it is time to make a big move, driven by faction AI

class OutsideContextProblem(Event):
    pass
    #Do you get the reference?
        #Big things, that really shake the world up. Late game content.

    """ event_registry = {
        "random": [Blackout, SolarFlare, CityFestival],
        "state": [MilitaryParade, TaxAudit],

    } """

    def apply(self, target):
            """Apply the effect to a single target (e.g., a character or faction)."""
            if self.event_type == "normal":
                impact_value = generate_normal(self.params.get("mean", 1), self.params.get("std_dev", 0.5))
            elif self.event_type == "black_swan":
                impact_value = generate_black_swan(self.params.get("threshold", 0.9), self.params.get("impact_range", (5, 20)))
            else:
                impact_value = 1  # default minimal impact

            self._apply_effect(target, impact_value)
            print(f"Event '{self.name}' occurred for {getattr(target, 'name', str(target))}! Impact: {impact_value}")

    def _apply_effect(self, target, impact):
        """Generic effect application."""
        if not self.effect:
            return

        if self.effect.get("impact") == "add":
            target[self.effect["resource"]] += impact
        elif self.effect.get("impact") == "subtract":
            target[self.effect["resource"]] -= impact
        elif self.effect.get("impact") == "modify":
            setattr(target, self.effect["attribute"], getattr(target, self.effect["attribute"]) + impact)
        else:
            raise ValueError(f"Unknown effect type: {self.effect.get('impact')}")        

    def resolve(self):
            """Override in subclasses for specific resolution logic."""
            pass

    def simulate_events(events, targets):
        """
        Simulate events and apply their effects to the targets.

        Args:
            events (list): A list of Event instances.
            targets (dict): A dictionary of targets (e.g., economy, factions).
        """
        for event in events:
            target_key = event.effect.get("resource") or event.effect.get("attribute")
            if not target_key:
                continue
            target = targets.get(target_key)
            if target:
                event.apply(target)



    def apply_to_faction(self, faction):
        """Apply event changes to a faction."""
        print(f"Applying event: {self.description}")
        for key, value in self.impact.items():
            if key in faction.resources:
                faction.resources[key] += value
                #When apply_to_faction() adds values, do some bounds checking (e.g., morale maxing at 100)
#combatEvent
#combatAftermath

class Robbery(Event):
    def __init__(self, instigator, location, weapon_used=False):
        """
        A Robbery event. Can be armed or unarmed.
        The event creates a Shop-like object to provide dynamic menu options and may involve intimidation.
        """
        super().__init__(
            name="Robbery",
            event_type="character",
            description=f"{instigator.name} is attempting to rob {location.name}.",
            effect={"impact": "modify", "attribute": "criminal_status"},
            impact={"criminal_status": 2},
            weapon_used=weapon_used
        )
        self.instigator = instigator
        self.location = location
        self.weapon_used = weapon_used
        self.shopkeeper = self._get_main_employee()
        self.bystander_attacked = False
        self.menu_options = []

    def affects(self, location):
        return self.location == location

    def update_menu_options(self): #player centric
        self.menu_options.clear()

        if self.location.characters_there and not self.bystander_attacked:
            self.menu_options.append("Attack Bystander") # might later be made possible to npc
        

    # Optionally: call this each tick or before menu render
    def get_menu_options(self):
        self.update_menu_options()
        return self.menu_options

    def _get_main_employee(self):

        if hasattr(self.location, "employees_there") and self.location.employees_there:
            return self.location.employees_there[0]
        return None
    
    def resolve(self, simulate=False, verbose=True):
        print(f"\n[Event]: {self.description}")
        self.apply(self.instigator)

        if not self.shopkeeper:
            print("No shopkeeper present. Robbery proceeds unopposed.")
            self.success = True
            return Burglary(
                name="Unopposed Robbery",
                instigator=self.instigator,
                location=self.location,
            )

        # Step 1: Attempt Intimidation

        weapon = getattr(self.instigator, "primary_weapon", None)
        weapon_name = weapon.name if weapon else "bare hands"
        
        intimidation_test = IntimidationTest(self.instigator, self.shopkeeper, wildcard_bonus=5)
        success = intimidation_test.run(simulate=simulate, verbose=verbose)
        
        if success:
            print(f"{self.instigator.name} successfully {color_text('intimidates', RED)} {self.shopkeeper.name} with {weapon_name}.")

        # Step 2: Steal physical cash if available
        if hasattr(self.location, "cash_register"):
            register = self.location.cash_register
            if register.cash > 0:
                cashwad = register.create_cashwad()
                self.instigator.inventory.add_item(cashwad)

                print(f"{self.instigator.name} steals ${cashwad.amount} from {self.location.name}!")
            else:
                print(f"The register at {self.location.name} is empty.")
        else:
            print(f"{self.location.name} has no cash register.")

        if hasattr(self.location, "inventory"):
            if hasattr(self, "target_item") and self.target_item in self.location.inventory.items:
                self.location.inventory.remove(self.target_item)
                self.instigator.inventory.add_item(self.target_item)
                print(f"{self.instigator.name} steals the targeted {self.target_item.name}!")

            for item in self.location.inventory.items.copy():
                if item is self.target_item:
                    continue  # Already taken
                if isinstance(item, ObjectInWorld):
                    self.location.inventory.remove(item)
                    self.instigator.inventory.add_item(item)
                    print(f"{self.instigator.name} also steals a {item.name}!")
                else:
                    print(f"{self.shopkeeper.name} resists the robbery attempt!")
                    # Trigger response
                    if hasattr(self.shopkeeper, "alert"):
                        self.shopkeeper.alert(self.instigator)
                    else:
                        print("xShopkeeper is panicking or shouting!")

        # Step 4: Witnesses respond
        witnesses = self.location.list_characters(exclude=[self.instigator])

        seen = set()
        reactions = []

        for witness in witnesses:
            witness.attention_focus = self.instigator
            #use @attention_focus.setter
            if id(witness) in seen:
                continue
            seen.add(id(witness))

            region = getattr(self.location, "region", "unknown")

            # Build a single percept dict describing the robbery, an active, event‐driven injection
            robbery_percept = {
                "description": f"Robbery at {self.location.name}",
                "origin": self,
                "tags": ["crime", "robbery"],
                "salience": 1.3,
                "location": self.location.name,
                "region": region,
                "weapon": {
                "name": weapon.name if weapon else None,
                "type": weapon.item_type if weapon else "none",
                "intimidation": getattr(weapon, "intimidation", 0) if weapon else 0,
                # ...any other fields...
            },
        }

        # Optional enhancement: add the class name of the weapon as a lowercase tag
        if weapon:
            robbery_percept["tags"].append("armed" if weapon else "unarmed")

        witness.perceive_event(robbery_percept)

        witness.fun = max(0, witness.fun - 5)

        # Approximate description
        appearance = self.instigator.get_appearance_description()

        #Should the below witness memory and thought go through the percept setter?

        appearance = self.instigator.get_appearance_description()
        witness.memory.add_entry(MemoryEntry(
            subject=self.instigator,
            object_="Robbery",
            details="Robbery witnessed",
            importance=8,
            type="crime_observed",
            target=self.instigator,
            approx_identity=self.instigator.get_appearance_description(),
            description=f"Witnessed a {appearance} commit a robbery at {self.location.name}",
            initial_memory_type="episodic"
        ))

        print(f"[MEMORY] {witness.name} will remember this episode involving {self.instigator.name} at {self.location.name}.")
        #todo, do they know his name though?

        if getattr(witness, "observation", 0) >= 2:
            witness.alert = True
            reactions.append((
                witness.name,
                "becomes alert and distressed!",
                witness.__class__.__name__
            ))

        #  Print reactions once, after loop

        for line in group_reactions(reactions):
            print(line)

        # ✅ Hook: handle security if present
        if hasattr(self.location, "security") and self.location.security.guards:
            print("[SECURITY] Guards are being alerted!")
            for guard in self.location.security.guards:
                # Add a placeholder call for now
                guard.respond_to_event(self)


                # Only print once, after all observations
                #from output_utils import group_reactions
                if hasattr(self, "observation_log"):
                    for line in group_reactions(self.observation_log):
                        print(line)

        # Step 5: Return ArmedRobbery object
        if self.weapon_used:
            return ArmedRobbery(self, self.instigator, self.location, weapon)

        
    def conclude(self):
        print(f"[DEBUG] Robbery at {self.location.name} is over. Returning to normal.")
        # This is a good hook to trigger narrative objects or AI response

    def record_observation(self, observer, instigator, region, location):
        """
        Collect observation data during event. Later, we'll summarize it.
        """
        if not hasattr(self, "observation_log"):
            self.observation_log = []

        reaction = None
        if getattr(observer, "observation", 0) >= 6:
            reaction = "becomes alert and distressed!"

        self.observation_log.append((
            observer.name,
            reaction,
            observer.__class__.__name__
        ))

        # Characters still suffer a small consequence
        observer.fun = max(0, observer.fun - 5)
        # === Aftermath cleanup ===
        for character in self.location.list_characters():
            if character.alert:
                character.alert = False  # 🔴 Reset alert after robbery ends

        # Hook to notify game_logic or narrative system
        self.conclude()

# Optionally: remove this event from active memory
# e.g., game_state.active_events.remove(self)

class Burglary(Event):
    def __init__(self, name, instigator, location, time=None, loot=None):
        self.name = name
        self.instigator = instigator
        self.location = location
        self.time = time  # optional, e.g., current tick or timestamp
        self.loot = loot if loot else []  # list of stolen items

    def __str__(self):
        return f"Burglary({self.name}) by {getattr(self.instigator, 'name', 'Unknown')} at {self.location.name}"

class Riot(Event):
    pass

class ArmedRobbery(Event):
    def __init__(self, instigator, location, weapon=None):
        super().__init__()
        self.instigator = instigator
        self.location = location
        self.weapon = weapon

    def get_percept(self):
        """Return a basic percept for the robbery event."""
        return {
            "description": f"Armed robbery by {self.instigator.name} at {self.location.name}",
            "tags": ["crime", "robbery", "armed"],
            "salience": 1.5,
            "location": self.location.name,
            "weapon": {
                "name": self.weapon.name if self.weapon else None,
                "type": self.weapon.item_type if self.weapon else "none",
                "intimidation": getattr(self.weapon, "intimidation", 0) if self.weapon else 0,
            }
        }
    
    def resolve(self):
        #needed to satisify ABC upstream
        # This could return a result or just log that it's a resolved object.
        print(f"[INFO] ArmedRobbery at {self.location.name} already resolved.")
        return "resolved"

    def handle_event(event_name, character, location):
        if event_name == "Rob":
            robbery = Robbery(character, location, weapon_used=True)
            incident = robbery.resolve()
            if incident:
                incident.resolve()
            return robbery
        else:
            print(f"Unhandled event type: {event_name}")


    def simulate_events(events, targets):
        for event in events:
            target = targets.get(event.effect.get("resource") or event.effect.get("attribute"))
            if target:
                event.apply(target)

class TurfWar(Event):

    #Set region.turf_war_triggered = True HERE, not evaluate

    def __init__(self, region, **kwargs):
        super().__init__(
            name="Turf War",
            event_type="incident",  # e.g. "incident", "normal", etc.
            description="Too many street gangs lloking for a home.",
            impact={"fun": -1},  # Replace or remove as needed
            **kwargs
        )
        self.region = region

    def raid():
        #increase steet_gang aggression vs other street_gangs, gangs, and raid buildings

        pass

    def generate_percepts(self):

        percept = {
            "description": f"{self.name} at {self.location.name}",
            "origin": self,
            "tags": ["template", "event"],
            "salience": 1.2,
            "location": self.location.name,
            "region": getattr(self.location, "region", "unknown"),
        }

    def conclude(self):
        #when there is <3 street gangs in a region,  conclude
        print(f"[DEBUG] {self.name} at {self.location.name} has concluded.")
        # Optional cleanup or progression logic here

class GangWar(Event): #or possibly define a Conflict base/intermediary class
    pass
    #initiative, momentum