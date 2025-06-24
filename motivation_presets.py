#motivation_presets.py
#I am not sure if this entire file is now legacy code and unused
from motivation import Motivation

#class presets, under structural development, specifics not relevant to Luna
class MotivationPresets:
    
    #old 
    """ tag_to_motivation = {
                        "rob": "rob",
                        "steal": "steal",
                        "weapon": "obtain_ranged_weapon",
                        "shop": "visit_location",
                        "explore": "visit_location",

                    } """

    @classmethod
    def tag_to_motivation(cls):
        return
    tag_to_motivation_presets = {
    "rob": Motivation("rob", 4, status_type="criminal"), #does the ai actually need status_type?
    "steal": Motivation("steal", 4, status_type="criminal"),
    "weapon": Motivation("obtain_ranged_weapon", 4),
    "shop": Motivation("visit", 4),
    "explore": Motivation("visit", 4),
    }
    
    _presets = {

        "GangMember": [
            Motivation("join_gang", 6, target="Red Fangs"),
            Motivation("obtain_ranged_weapon", 5),
            Motivation("increase_status", 4, status_type="criminal"),
            Motivation("steal_money", 4, status_type="criminal"),
            Motivation("rob", 4, status_type="criminal"),
        ],

        "Manager": [
                Motivation("join_corporation", 2, target="good question"),
                Motivation("virtue_signal", 5),
                Motivation("increase_status", 4, status_type="corporate"),
                Motivation("have_fun", 4, status_type="good question"),
            ],

        "CorporateSecurity": [
            Motivation("protect_location", 6),
            Motivation("protect_allies", 5, status_type="corporate"),
        ],

        "CorporateAssassin": [
                Motivation("obtain_contract", 6),
                Motivation("assassinate_target", 0, status_type="corporate"),
                Motivation("earn_money", 6),
                Motivation("increase_status", 6),
            ],

        "Civilian": [
                Motivation("earn_money", 3),
                Motivation("have_fun", 6, status_type="corporate"),
                Motivation("protect_family", 6),
                Motivation("increase_status", 2),
            ],       
            
        "Player": [
            Motivation("explore_city", 5),
            Motivation("earn_money", 4),
        ],

        "RiotCop": [
            Motivation(type="enforce_law", urgency=5),
            Motivation(type="earn_money", urgency=4)
                ],
        "Detective": [
            Motivation(type="enforce_law", urgency=6),
            Motivation(type="earn_money", urgency=3)
        ],
        "Taxman": [
            Motivation(type="gain_money", urgency=5),
            Motivation(type="squeeze_taxes", urgency=6)
        ],
        "Employee": [
            Motivation(type="gain_money", urgency=4),
            Motivation(type="gain_status", urgency=3)
        ],

        "CEO": [
            Motivation(type="increase_profits", urgency=5),
            Motivation(type="gain_elite", urgency=4)
        ],

        "Accountant": [
            Motivation(type="reduce_taxes", urgency=4),
            Motivation(type="earn_money", urgency=3)
        ],

        "Boss": [
            Motivation(type="gain_high", urgency=5),
            Motivation(type="recruit_members", urgency=3),
            Motivation(type="increase_criminal_status", urgency=4)
        ],

        "Captain": [
            Motivation(type="gain_high", urgency=4),
            Motivation(type="execute_orders", urgency=3)
        ],

        "SpecialChild": [
                Motivation("explore_math", 10),
                Motivation("have_fun", 2),
                Motivation("use_advanced_python_features", 10),
                Motivation("stimulate_program", 2), #stimulate irl AI, and help me learn
                Motivation("eat", 2),
                Motivation("sleep", 2),
                Motivation("shelter", 2),
            ],

        "Adepta": [
                Motivation("earn_money", 3),
                Motivation("have_fun", 6, status_type="civilian"),
                Motivation("charm U7s", 20),
                Motivation("increase_status", 2),
            ],

    }



    @classmethod
    def for_class(cls, class_name: str):
        return cls._presets.get(class_name, [])
