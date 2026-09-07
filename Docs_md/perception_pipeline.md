#Docs_md.perception_pipeline.md
# Perception Pipeline

## Philosophy

The GUI should not inspect the simulation directly.

Instead, information should flow through a single perception pipeline.

The simulation produces perceptual information for an observing character. The GUI then transforms that information into presentation-oriented ViewModels and display structures.

```text
Simulation
    ↓
ObservationComponent.observe()
    ↓
observer.percepts
    ↓
build_percept_sections()
    ↓
build_percept_tree()
    ↓
DisplayNode tree
    ↓
display transformations
    ├── aggregation
    └── other presentation transformations
    ↓
GUI renderer
    ↓
Tkinter GUI
```

This creates a separation between three concerns:

1. **Simulation / perception**

   * Simulation objects know how to describe themselves perceptually.
   * `ObservationComponent` gathers what an NPC can perceive.
   * `observer.percepts` contains the resulting percept records.

2. **Presentation transformation**

   * ViewModels and `DisplayNode` structures transform percept data into GUI-oriented representations.
   * Parent/child relationships such as `resting_on` are represented here.
   * Low-value repeated percepts may be aggregated here.
   * Presentation decisions such as aggregation should not be pushed back into the simulation layer.

3. **GUI rendering**

   * The renderer consumes the presentation structures.
   * Tkinter-specific operations such as `tree.insert()` belong here.
   * The renderer should not need to search the simulation world to discover what an NPC can perceive.

## Important distinction: percepts vs display representations

A percept represents something the NPC knows about.

A display representation represents how that knowledge should be presented to a human user.

For example, an NPC may perceive:

```text
Table 2
Table 3
Table 4
Table 5
Table 7
Table 8
```

as six separate percepts.

The GUI may reasonably transform those low-information percepts into:

```text
Tables (x6)
```

This does not mean the NPC perceives "Tables (x6)". It is a presentation transformation applied after perception.

Conversely, a table containing a perceptible object may remain an individual display node:

```text
Table 1
    Cup
```

because the relationship provides useful information.

## DisplayNode

`DisplayNode` represents a presentation-level tree.

It currently derives its identity and data from a percept:

```text
percept
    ↓
DisplayNode
    ├── percept
    └── children
```

The tree can represent relationships expressed by percept data, such as:

```python
data["resting_on"] = supporting_object
```

This allows the GUI to display:

```text
Expensive Desk
    Gold-Plated Pistol
    Advanced Medkit
```

without the tree-building code needing to know what a desk, pistol, or medkit is.

## Display aggregation

Aggregation is a presentation transformation.

For example:

```text
CafeTable Table 2
CafeTable Table 3
CafeTable Table 4
...
```

may become:

```text
Tables (x6)
```

while significant individual nodes remain separate:

```text
Table 1
    Cup

Table 6
    Ceramic Vase
```

The aggregation code operates on `DisplayNode` objects rather than modifying the underlying simulation objects.

This preserves the distinction between:

```text
what the NPC perceives
```

and:

```text
how that perception is presented to the human user
```


---




## Observation

Characters observe the world using:

```python
ObservationComponent.observe()
```

Observed entities provide their own percept data via:

```python
get_percept_data(observer)
```

Objects decide how they appear to observers.

The ObservationComponent stores percepts but should avoid generating
object-specific presentation data.

---

## ViewModels

ViewModels transform percepts into structures that are convenient for the GUI.

Examples:

- SublocationViewModel
- (future) CharacterViewModel
- (future) LocationViewModel

ViewModels should:

- filter percepts
- aggregate percepts
- prepare display data

They should not inspect the simulation directly whenever percept data already
exists.

---

## GUI

The GUI should consume ViewModels rather than simulation objects.

Tkinter code should focus on presentation.

Examples:

- treeviews
- labels
- notebooks
- buttons

Business logic should remain outside GUI code.

---

## Architectural Principle

Avoid this:

```
Simulation
      ↘
Observation
      ↘
GUI
```

Prefer:

```
Simulation

↓

Observation

↓

ViewModel

↓

GUI
```

This makes perception rules consistent and keeps presentation separate from
simulation.
