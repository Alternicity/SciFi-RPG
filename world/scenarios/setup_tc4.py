#world.scenarios.setup_tc4.py

from create.create_game_state import get_game_state
gs = get_game_state()
from faction import Gang
from characters import GangMember, Captain, Boss
from world.placement import place_character_in_sublocation
from social.social_utils import link_relationship

from objects.unique_objects import GoldPlatedPistol

from objects.furniture import CafeChair
from objects.furniture import Chair

from objects.expensive_furniture import ExpensiveDesk
from augment.augmentLocations import add_office_furniture
from social.social_utils import link_relationship, create_social_group
from world.scenarios.setup_tc4_helpers import select_tc4_gang
from world.scenarios.setup_tcX_helpers import register_scenario_npc
from world.scenarios.tc4_memory_setup import seed_tc4_boss_memory
from augment.augmentSublocations.augmentGangSublocations import augment_gang_hq_sublocations
from world.place_objects import place_object
from actions.npc_bodily_actions import sit_on
from objects.expensive_furniture import OrnateChair
from character_components.npc_effects import Inebriated

#setup gang meeting

#the boss has summoned his Captains, someone is inebriated:
def setup_tc4_world(all_characters):
    #I must exclude reserved GangMembers who are used in tc2 via gamestate.is_scenario_npc or debug_npcs
    #gang = select_tc4_gang()

    #the reservation is this
    gang = gs.test_world["gang"]

    #get the gang details in compact form
    hq = gang.HQ
    #alternatively:
    #hq = gs.test_world["hq"]
    race = gang.race

    boss = gang.boss#we could use gang.get_leader. Does this duplicate earlier selection code? 
    captains = gang.captains #list, we could use gang.get_mid_tier()
    members = gang.members #list, we could use gang.get_workers()
    #or maybe we could use gang.iter_hierarchy() or these 3

    inebriated_npc = captains[0]

    inebriated = Inebriated()
    inebriated_npc.effects.append(inebriated)
    inebriated.on_start(inebriated_npc)


    is_street_gang = gang.is_street_gang #bool ATTN
    #if True, we need to discard this gang and choose another. The gang for this file needs to have a HQ

    goal = None
    goal_status = None

    gang.is_vengeful = True
    gang.violence_disposition += 5
    
    #enemies = {}#this exists in class Faction, which Gang inherits from
    #I will need to learn how to set this up here vs rival gangs, corporations, the State faction etc
    #It might need to become an object rather than a dict

    #maybe move to augment_hq.py when tc4 and general gang hq diverge
    bosses_office = next(
            (
                subloc
                for subloc in hq.sublocations
                if subloc.name == "Boss Office"
            ),
            None
        )
    
    if bosses_office:
        augment_gang_hq_sublocations(bosses_office)
        #this will eventuall draw on faction semiotics using somehitng more like:
        #decorate_hq_for_faction(hq)

    if boss:

        register_scenario_npc(boss, "TC4 Boss")
        #Use register_scenario_npc() for all TCx_setup
        seed_tc4_boss_memory(
            boss,
            gang
        )

        boss_chair = next(
            (
                obj
                for obj in bosses_office.items.objects_present
                if isinstance(obj, OrnateChair)
            ),
            None,
        )

        boss_desk = next(
                    (
                        obj
                        for obj in bosses_office.items.objects_present
                        if isinstance(obj, ExpensiveDesk)
                    ),
                    None,
                )
        pistol = GoldPlatedPistol()
        pistol.change_ownership(boss)
        place_object(pistol, bosses_office)
        boss_desk.add_to_surface(pistol)

        if boss_chair:
            sit_on(boss, boss_chair)
            #Add relationship with Desk
            #associate_furniture(boss_chair, boss_desk) for example

    office_chairs = [
        obj
        for obj in bosses_office.items.objects_present
        if isinstance(obj, Chair)
        and not isinstance(obj, OrnateChair)
    ]

    for captain, chair in zip(captains, office_chairs):

        sit_on(captain, chair)
        """ zip() is nice here because if you have three captains and six chairs, only three are used. 
        If you later have eight captains and six chairs, the remaining captains simply won't be seated. """

    remaining_chairs = office_chairs[len(captains):]

    for member, chair in zip(members, remaining_chairs):

        sit_on(member, chair)
    


    #All Captains and GangMembers will need to be added to game state and become scenario_npc = True like this
    #Probably in a loop here

    for captain in captains:
        
        register_scenario_npc(
            captain,
            "TC4 Captain"
        )

        link_relationship(
            boss,
            captain,
            relation_type="leader",
            familiarity=7,
            trust=7,
            respect=8,
            fear=3,
            interest=5,
        )

        link_relationship(
        captain,
        boss,
        relation_type="subordinate",#Correct? Captain is subordinate to a Boss
        familiarity=8,
        trust=8,
        respect=10,
        fear=6,
    )

    for member in members:#call in the same ways as Captains
        
        register_scenario_npc(
            member,
            "TC4 Ganger"
        )

        link_relationship(
            boss,
            member,
            relation_type="leader",
            familiarity=7,
            trust=7,
            respect=8,
            fear=2,
            interest=5,
        )

        link_relationship(
        member,
        boss,
        relation_type="subordinate",
        familiarity=8,
        trust=8,
        respect=10,
        fear=8,
    )

    meeting_attendees = [
        boss,
        *captains,#*creates a list
        *members
    ]

    meeting_group = create_social_group(*meeting_attendees, label="Meeting", purpose="Planning", interaction_targets=False,)
    #In this context, * means unpack this iterable into positional arguments.
    #Notice interaction targets are disabled.

    for npc in meeting_attendees:

        place_character_in_sublocation(
            npc,
            bosses_office,
        )
    #This
    """ for npc in meeting_attendees:

        npc.is_scenario_npc = True

        npc.debug_role = f"tc4_{npc.__class__.__name__.lower()}"

        gs.debug_npcs[npc.debug_role] = npc """

    #motivations
    boss.motivation_manager.update_motivations(

        "HoldMeeting",

        target=meeting_group,

        urgency=8,

    )

    for captain in captains:

        captain.motivation_manager.update_motivations(

            "AttendMeeting",

            target=meeting_group,

            urgency=7,

        )