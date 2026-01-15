#soul.py
class Soul:
    def __init__(self):
        self.ψ_core = True
        self.ψ_prana = 1.0
        self.ψ_chitti = 0.1
        self.ψ_karman = []
        self.ψ_ananda = 0.0
        self.ψ_dharmon = 0.0
        self.ψ_mneme = {}
        self.ψ_phone = []

    def inscribe_event(self, event, valence):
        # add to memory
        self.ψ_mneme[event] = valence
        # resonance update
        self.ψ_ananda += max(0, valence)
        self.ψ_dharmon += self.evaluate_alignment(event)
