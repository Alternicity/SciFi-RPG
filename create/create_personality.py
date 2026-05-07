#create.create_personality.py
import random
from character_components.personality.personality import Personality
from distributions import generate_stat

def generate_trait():#currently unused here, movebakc to distributions.py ?
    value = random.gauss(10, 3)
    return max(1, min(20, int(round(value))))


def create_personality(npc=None):

    return Personality(
        extroversion=generate_stat(),
        curiosity=generate_stat(),
        discipline=generate_stat(),
        agreeableness=generate_stat(),
        neuroticism=generate_stat()
    )