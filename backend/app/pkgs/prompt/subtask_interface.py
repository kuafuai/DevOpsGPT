from abc import ABC, abstractmethod

from config import GRADE

class SubtaskInterface(ABC):
    @abstractmethod
    def splitTask(self, requirementID, feature, serviceName, appBasePrompt, projectInfo, projectLib, serviceStruct, appID):
        pass

    @abstractmethod
    def splitTaskDo(self, requirementID, feature, serviceName, appBasePrompt, projectInfo, projectLib, serviceStruct, appID):
        pass

    @abstractmethod
    def write_code(self, requirement_id, service_name, file_path, development_detail, step_id):
        pass
