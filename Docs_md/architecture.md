#Docs_md.architecture.md

# TC2 Architecture Overview

## Core Philosophy

TC2 is a simulation-first sci-fi RPG focused on emergent NPC behaviour, faction dynamics, social systems, and psychological modelling.

The project prioritizes:

* emergent interactions
* meaningful world simulation
* inspectable/debuggable systems
* gradual architectural evolution
* LLM-assisted development

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

TC2 primarily uses Utility AI.

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

* gang structures
* status systems
* reputation
* territorial dynamics

## GUI Systems

Current GUI development focuses on:

* NPC inspection
* simulation observability
* debugging tools
* future player interaction

---

# Architectural Strategy

TC2 avoids large refactors unless necessary.

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
