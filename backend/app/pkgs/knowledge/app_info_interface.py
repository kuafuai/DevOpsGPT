from abc import ABC, abstractmethod

from config import GRADE

class AppInfoInterface(ABC):
    @abstractmethod
    def getAppArchitecture(self, appID):
        pass

    @abstractmethod
    def getServiceSwagger(self, apiDocUrl):
        pass

    @abstractmethod
    def getServiceBasePrompt(self, appID, serviceName):
        pass

    @abstractmethod
    def getServiceIntro(self, appID, serviceName):
        pass

    @abstractmethod
    def getServiceLib(self, appID, serviceName):
        pass

    @abstractmethod
    def getServiceSpecification(self, appID, serviceName, LibName):
        pass

    @abstractmethod
    def getServiceGitPath(appID, serviceName):
        pass

    @abstractmethod
    def getServiceDockerImage(appID, serviceName):
        pass