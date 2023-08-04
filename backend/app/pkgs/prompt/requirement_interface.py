from abc import ABC, abstractmethod

from config import GRADE

class RequirementInterface(ABC):
    @abstractmethod
    def clarifyRequirement(self, userPrompt, globalContext, appArchitecture):
        pass