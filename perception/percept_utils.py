#perception.percept_utils.py

#canonical coercion helper
def normalize_percept(percept_data, npc):
    """
    Return a safe percept dict with keys:
    { 'object', 'name', 'tags', 'origin', 'salience', 'details' }
    """
    #use _normalize_percept() in anchor methods

    # dict already
    if isinstance(percept_data, dict):
        p = dict(percept_data)  # shallow copy
        p.setdefault("object", p.get("origin", p.get("object")))
        p.setdefault("name", p.get("name", str(p.get('object', '<unknown>'))))
        p.setdefault("tags", p.get("tags", []))
        p.setdefault("salience", p.get("salience", 1.0))
        p.setdefault("origin", p.get("origin", p.get("object")))
        return p

    # objects that implement get_percept_data(observer=)
    if hasattr(percept_data, "get_percept_data"):
        try:
            p = percept_data.get_percept_data(observer=npc) or {}
            p.setdefault("object", percept_data)
            p.setdefault("name", getattr(percept_data, "name", str(percept_data)))
            p.setdefault("tags", getattr(percept_data, "tags", []))
            p.setdefault("salience", getattr(percept_data, "salience", 1.0))
            p.setdefault("origin", percept_data)
            return p
        except Exception:
            pass

    # fallback synthesis
    tags = list(getattr(percept_data, "tags", []) or [])
    name = getattr(percept_data, "name", None) or str(percept_data)
    return {
        "object": percept_data,
        "name": str(name),
        "tags": tags,
        "origin": getattr(percept_data, "origin", percept_data),
        "salience": getattr(percept_data, "salience", 1.0),
    }
    