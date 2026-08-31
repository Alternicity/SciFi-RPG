#Docs_md.architecture.md

# TC2 Architecture Overview

## Core Philosophy

The simulation-is focused on emergent NPC behaviour, faction dynamics, social systems, and psychological modelling.
TC1 is a GangMember centred development involving aquiring a ranged_weapon and robbing a shop. Likey currently broken
TC2, ie test case 2, is an npc normal life development - work, eat, have_fun and sleep. Rough draft is finished but needs polish
#GUI development with tkinter was happening in a decoupled way but reecntly necessitated a refactor in world setup and early program flow.

The project also emphasizes:

* clear separation of simulation and presentation
* observer-centric information flow
* reusable generic world systems
* avoiding scenario-specific logic in core simulation
* emergent interactions
* meaningful world simulation
* inspectable/debuggable systems
* gradual architectural evolution


The simulation is intended to support:

* civilian life simulation
* faction conflict
* economic systems
* social memory
* utility-driven AI
* psychological modelling
* future player interaction

---

# Core AI Direction

The sim primarily uses Utility AI.

NPCs evaluate:

* motivations
* thoughts
* urgency
* role context
* personality
* social pressures
* environmental conditions

Higher level NPCs may eventually:

* delegate tasks
* coordinate groups
* influence subordinate behaviour

without requiring entirely separate AI paradigms.

---

# Current Major Systems

## World Systems

* locations
* sublocations
* object placement
* ambience
* environmental props
* containers

## NPC Systems

* stats
* motivations
* thoughts
* anchors
* personality
* inventory
* employment
* social memory
* utility AI
* observation systems

## Faction Systems

* gang and corporation structures
* status systems
* reputation
* territorial dynamics

## GUI Systems

Current GUI development focuses on:

* observer-driven inspection
* entity navigation
* simulation observability
* debugging tools
* reusable inspectors
* future player interaction

---

# Architectural Strategy

Whenever practical, the project prefers a single canonical code path for common
operations.

Examples include:
Sim layer:
* ObservationComponent.observe()
* place_object()

GUI layer:
* show_entity_page()

This reduces duplicated logic and makes future systems easier to extend.

Preferred approach:

* additive evolution
* parallel tooling
* observability first
* incremental stabilization

The project values:

* simulation continuity
* debuggability
* system interoperability
* long-term extensibility

---

# Scenario / World Setup Architecture

create: What exists?
augment: What permanently fills it?
customize: How is it adapted for its owner or identity?
scenario: What is happening right now?

The simulation now supports modular world scenario setup.

Scenario modules live in:

world/scenarios/

Examples:

* setup_tc1.py
* setup_tc2.py
* setup_normal_stuff.py

These scenario modules:

* seed NPCs
* inject motivations
* place characters
* configure relationships
* augment regions
* prepare test environments
Scenario modules are responsible for configuring the world rather than extending
simulation behaviour.

Typical responsibilities include:

* selecting test factions
* selecting debug NPCs
* placing characters
* augmenting environments
* placing objects
* creating relationships
* seeding memories
* configuring test situations

Scenarios are applied during early startup:

main.py
→ setup_game()
→ apply_scenarios(all_characters)

This architecture allows:

* modular test cases
* future GUI toggles
* selective simulation presets
* cleaner separation of setup and runtime logic
* reduced simulation.py complexity
Scenario modules are responsible for:

* selecting debug/test NPCs
* assigning regions and locations
* injecting motivations
* seeding memories
* configuring employment
* placing furniture or environmental props
* creating special test conditions

Scenario setup occurs before simulation ticks begin.

Current scenarios include:

* TC1 — gang/crime behaviour testing
* TC2 — civilian normal life simulation

Scenarios are applied through:

apply_scenarios(all_characters)

Long-term direction may include:

* pluggable world modules
* faction injectors
* economic presets
* government systems
* environmental modifiers
* corporation/worldpack style additions

# Information Flow

The project is gradually moving toward a unified data flow.

Simulation

↓

Observation

↓

ViewModels

↓

GUI

Whenever possible, GUI code should consume ViewModels built from observer
percepts rather than querying simulation objects directly.

This keeps perception rules centralized and ensures the GUI represents what an
observer actually knows.