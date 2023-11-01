from abc import ABC, abstractmethod

from config import GRADE


class AppInfoInterface(ABC):
    @abstractmethod
    def getServiceLib(self, appID, serviceName):
        pass

    @abstractmethod
    def getServiceStruct(self, appID, serviceName):
        pass

    @abstractmethod
    def getServiceSpecification(self, appID, serviceName, LibName):
        pass

    @abstractmethod
    def analyzeService(self, tenant_id, git_path):
        pass


    def repo_analyzer(self, type, repo, task_id):
        pass