#social_utils.py
#in the root folder for now at least
from focus_utils import set_attention_focus
class Interaction:
    def __init__(self, a, b, context=None):
        self.a = a
        self.b = b
        self.context = context
        self.first_encounter = not a.knows(b)
        self.opinion_delta = {}

    def begin(self):
        set_attention_focus(self.a, self.b)
        set_attention_focus(self.b, self.a)

        self.form_first_impression()

class ServiceInteraction(Interaction):
    def apply_norms(self):
    #politeness, service hierarchy