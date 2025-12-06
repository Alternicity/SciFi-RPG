#SPARE

def generate_thoughts_from_percepts(self):
    npc = self.npc
    thoughts = []
    
    # Use internal values safely
    percepts = list(npc.observation_component._percepts.values())  
    
    motivations = npc.motivation_manager.get_urgent_motivations()
    
    for percept in percepts:
        for motive in motivations:
            salience = compute_salience(percept, motive)
            if salience < 5:
                continue

            thought = Thought(
                subject=npc.name,
                content=percept.get("description", "unknown"),
                origin=percept.get("origin"),
                urgency=salience,
                tags=percept.get("tags", []),
                source=motive  # Optional
            )

            if not npc.mind.has_similar_thought(thought):
                npc.mind.add_thought(thought)
                print(f"[THOUGHT] {npc.name} thought: {thought.content} (salience: {salience})")
