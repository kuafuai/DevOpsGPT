from abc import ABC, abstractmethod

from config import GRADE

class SubtaskInterface(ABC):
    @abstractmethod
    def splitTask(self, requirementID, feature, serviceName, appBasePrompt, projectInfo, projectLib, serviceStruct, appID):
        pass