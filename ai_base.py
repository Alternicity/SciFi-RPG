from abc import ABC, abstractmethod

class BaseAI(ABC):
    @abstractmethod
    def choose_action(self, character, region):
        pass