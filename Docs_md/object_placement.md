#Docs_md.object_placement.md

# Object Placement

## Purpose

All world objects should be placed using a single placement function.

The goal is to ensure every object has consistent world metadata regardless of
whether it is placed in a Location or a Sublocation.

Current placement helper:

```python
place_object(obj, destination)
```

---

## Why

Historically, objects were manually inserted into locations.

Example:

```python
chair.location = room
chair.region = room.region
room.items.objects_present.append(chair)
```

This worked for Location objects, but failed for Sublocations because
`chair.sublocation` was never assigned.

This caused perception bugs where:

- the object existed in the simulation
- ObservationComponent observed it
- but the percept contained

```
sublocation = None
```

The GUI ViewModel therefore filtered the object out.

---

## Canonical Placement

Every object should be placed through:

```python
place_object(obj, destination)
```

The helper is responsible for assigning:

- region
- location
- sublocation

before inserting the object into:

```
destination.items.objects_present
```

No code outside the placement helper should manually assign these fields unless
there is a specific reason.

---

## Design Goals

The placement system should be:

- generic
- scenario-independent
- reusable by all world generation

It should support:

- Locations
- Sublocations

without special-case scenario logic.

---

## Future

Possible future additions:

- move_object()
- remove_object()
- transfer_object()

These should reuse the same placement rules.
