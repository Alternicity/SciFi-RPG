
#code cut from class character during a refactor

from behaviour.behaviours import set_default_behaviour, BehaviourManager
        self.behaviors = set(behaviors) if behaviors else set_default_behaviour()
        self.behaviour_manager = BehaviourManager()


