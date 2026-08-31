#customize.customize_hq_for_owner.py
from create.create_sublocations import create_boss_office, create_executive_office


def customize_hq_for_owner(hq):
    if hq.faction.type == "gang":

        create_boss_office(hq)

    elif hq.faction.type == "corporation":

        create_executive_office(hq)

        