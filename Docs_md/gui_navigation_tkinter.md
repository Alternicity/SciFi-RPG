#Docs_md.gui_navigation_tkinter.md

# GUI Navigation

## Philosophy

The GUI is moving away from page-specific navigation.

Instead, navigation is entity-driven.

Rather than calling:

```python
show_sublocation_center_view()
```

the GUI should call:

```python
show_entity_page(observer, entity)
```

The dispatcher selects the correct builder.

---

## Entity Dispatcher

Current pattern:

```python
show_entity_page(observer, thing)
```

Examples:

- Character
- Sublocation
- SocialGroup

Future:

- Location
- Region
- Faction
- Business
- Vehicle

---

## Observer

Every entity page should receive:

```python
observer
```

The observer represents the active NPC.

Pages should display information available through that NPC's percepts.

The observer is therefore part of navigation context.

---

## Inspector vs Entity Page

The inspector displays a summary of the currently selected entity.

Entity pages provide a full-page view.

Selection should not directly inspect simulation objects when percept data is
available.

---

## Active Context

The GUI maintains navigation state using:

```
active_context
```

This records the current observer and navigation mode.

Entity pages should derive their data from this context rather than performing
new simulation queries.

---

## Long-term Goal

Every inspectable object should eventually use the same navigation path.

```
Character
Location
Sublocation
Faction
SocialGroup
Business
Vehicle
...
```

Adding a new inspectable entity should only require:

1. ViewModel
2. Entity page builder
3. Dispatcher registration