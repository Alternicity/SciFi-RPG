from distributions import generate_normal, generate_black_swan
from combat import calculate_intimidation_score, calculate_resistance_score
from characterActionTests import IntimidationTest
from InWorldObjects import ObjectInWorld
from visual_effects import loading_bar, RED, color_text
from abc import ABC, abstractmethod

class Event(ABC):
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
    
    def handle_event(event_name, character, location):
        if event_name == "Rob":
            robbery = Robbery(character, location, weapon_used=True)
            incident = robbery.resolve()

            if incident:
                incident.alert_authorities()
                Event.trigger_event_outcome(character, "incident", location)
                #trigger_event_outcome is marked as not defined here
            return robbery
        
    @staticmethod
    def handle_incident(character, location=None):
        location = location or character.location  # fallback if None
        severity = 2  # or dynamic
        incident = Incident(name="Suspicious Activity", instigator=character, location=location, severity=severity)
        incident.resolve()

    @staticmethod
    def get_character_driven_event_outcomes(character, location=None):
        return {
            "success": lambda: print(f"{character.name} successfully completes the action."),
            "detected": lambda: print(f"{character.name} was spotted! Guards are alerted."),
            "parsimony_opportunity": lambda: print(f"{character.name} notices another opportunity."),
            "triggered_trap": lambda: print(f"{character.name} sets off a trap! Trouble ahead."),
            "incident": lambda: Event.handle_incident(character, location)
            #handle_incident marked as not defined
            #apparently handle_incident being not defined is ok bc its a lambda
            
        }
    @staticmethod
    def trigger_event_outcome(character, event_name, location=None):
        outcomes = Event.get_character_driven_event_outcomes(character, location)

        #get_character_driven_event_outcomes is marked as not defined
        outcomes.get(event_name, lambda: print(f"Unknown event outcome: {event_name}"))()


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
        The event targets a Shop-like object to provide dynamic menu options and may involve intimidation.
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
        self.bystander_attacked = False  # This could be changed by actions
        self.menu_options = []  # will be dynamically updated

        # Also perhaps add characters_there so later witnesses code will be able to populate it

    def affects(self, location):
        return self.location == location

    def update_menu_options(self):
        self.menu_options.clear()

        if self.location.characters_there and not self.bystander_attacked:
            self.menu_options.append("Attack Bystander")
        
        # More event-driven options can be added here as needed

    # Optionally: call this each tick or before menu render
    def get_menu_options(self):
        self.update_menu_options()
        return self.menu_options

    def _get_main_employee(self):
        """
        Returns the first employee present at the location, if any.
        Later we might choose based on role or status.
        """
        if hasattr(self.location, "employees_there") and self.location.employees_there:
            return self.location.employees_there[0]
        return None
    
    def resolve(self, simulate=False, verbose=True):
        print(f"\n[Event]: {self.description}")
        self.apply(self.instigator)

        if not self.shopkeeper:
            print("No shopkeeper present. Robbery proceeds unopposed.")
            self.success = True
            return Incident(
                name="Unopposed Robbery",
                instigator=self.instigator,
                location=self.location,
                severity=1
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
                        print("Shopkeeper is panicking or shouting!")

        # Step 4: Witnesses respond
        witnesses = self.location.list_characters(exclude=[self.instigator])
        for witness in witnesses:
            region = self.location.region if hasattr(self.location, "region") else "unknown"
            witness.observe("robbery", self.instigator, region, self.location)

            witness.fun = max(0, witness.fun - 5)
            print(f"{witness.name} witnesses the robbery and becomes distressed!")
            #reaction and memory code
            #if instigator sees (observe) the witness try to call the cops with their SmartPhone, add another menu option
            #for instigator to react, maybe another intimidate() "Dont do it!" ,and attack option. robbers are cold.

        # Step 5: Return Incident object
        if self.weapon_used:
            return Incident("Armed Robbery", self.instigator, self.location, severity=3)
        else:
            return Incident("Attempted Robbery", self.instigator, self.location, severity=2)
    
class Incident(Event):
    def __init__(self, name, instigator, location, severity=1):
        super().__init__(
            name=name,
            event_type="incident",
            description=f"An incident occurred at {location.name} caused by {instigator.name}.",
            effect={"impact": "modify", "attribute": "heat"},
            impact={"heat": severity}
        )
        self.instigator = instigator
        self.location = location
        self.severity = severity

    def resolve(self):
        print(f"[Incident] {self.description}")
        self.apply(self.instigator)
        self.alert_authorities()

    def alert_authorities(self):
        print(f"Authorities alerted due to severity {self.severity}!")
        if hasattr(self.location, "call_police"):
            self.location.call_police()

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