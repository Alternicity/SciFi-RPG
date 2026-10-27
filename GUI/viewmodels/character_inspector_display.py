# GUI/viewmodels/character_inspector_display.py
from dataclasses import dataclass, field
from status import get_primary_status_display

@dataclass
class InspectorSection:
    label: str
    value: str


@dataclass
class CharacterInspectorViewModel:
    name: str
    sections: list[InspectorSection] = field(default_factory=list)


def get_character_inspector_data(npc, observer=None):
    """
    Pure data assembly for the NPC inspector (right panel).

    Semantic percept -> labeled sections. Rendering is the caller's job.
    """
    percept = npc.get_percept_data(observer=observer)

    sections: list[InspectorSection] = []

    # Observed traits (rendered as a single comma-joined line, matching old behavior)
    observable = percept.get("observable_traits", [])
    if observable:
        sections.append(InspectorSection(
            label="Observed",
            value=", ".join(observable),
        ))

    if percept.get("race"):
        sections.append(InspectorSection(label="Race", value=percept["race"]))

    if percept.get("sex"):
        sections.append(InspectorSection(label="Sex", value=percept["sex"]))

    # bloodstained / is_visibly_wounded will arrive via _postprocess_percept (TC4).
    # Rendered conditionally if present in the percept.
    if percept.get("bloodstained"):
        blood = percept["bloodstained"]
        who = getattr(blood, "name", blood)
        sections.append(InspectorSection(label="Bloodstained", value=str(who)))

    if percept.get("is_visibly_wounded"):
        sections.append(InspectorSection(label="Wounded", value="yes"))

    if percept.get("posture") is not None:
        sections.append(InspectorSection(
            label="Posture",
            value=percept["posture"].name.title(),
        ))

    if percept.get("seated_at") is not None:
        sections.append(InspectorSection(
            label="Seated at",
            value=percept["seated_at"].name,
        ))

    # TODO: effects currently scrape simulation objects (npc.effects).
    # Eventually surface via percept. Keep here for now.
    for effect in npc.effects:
        symptoms = effect.visible_symptoms()
        if symptoms:
            sections.append(InspectorSection(
                label="Effect",
                value=", ".join(symptoms),
            ))

    # Relation block. Read relations dict directly; never call get_relation()
    # (which creates records as a side-effect).
    rel = None
    if observer is not None and hasattr(observer, "social_memory"):
        rel = observer.social_memory.relations.get(npc.id)

    if rel:
        sections.append(InspectorSection(
            label="Relation",
            value=rel.current_type,
        ))
        # Only show scalars if familiarity is above some threshold
        if rel.familiarity >= 3:
            sections.append(InspectorSection(
                label="Trust",
                value=f"{rel.trust}  Familiarity: {rel.familiarity}",
            ))
            sections.append(InspectorSection(
                label="Affection",
                value=f"{rel.affection}  Fear: {rel.fear}",
            ))
        if rel.past_types:
            sections.append(InspectorSection(
                label="Previously",
                value=", ".join(rel.past_types),
            ))
    else:
        sections.append(InspectorSection(label="Relation", value="unknown"))

    status_text = get_primary_status_display(npc)
    sections.append(InspectorSection(label="Status", value=str(status_text)))

    # TODO: access_component is a simulation object; eventually via percept.
    access = getattr(npc, "access_component", None)
    if access:
        sections.append(InspectorSection(label="Access", value=str(access)))

    return CharacterInspectorViewModel(name=npc.name, sections=sections)
