from app.models.app import App
from app.pkgs.knowledge.app_info_interface import AppInfoInterface

class AppInfoPro(AppInfoInterface):
    def getAppArchitecture(self, appID):
        # The current version does not support this feature
        return "", False
    
    def getServiceSwagger(self, appID, serviceName):
        # The current version does not support this feature
        return "", False

    def getServiceBasePrompt(self, appID, serviceName):
        # The current version does not support this feature
        return "", False


    def getServiceIntro(self, appID, serviceName):
        # The current version does not support this feature
        return "", False
    
    def getServiceLib(self, appID, serviceName):
        # The current version does not support this feature
        return "", False

    def getServiceStruct(self, appID, serviceName):
        # The current version does not support this feature
        return "", False

    def getServiceSpecification(self, appID, serviceName, LibName):
        # The current version does not support this feature
        return "", False

    def getServiceGitPath(self, appID, serviceName):
        # The current version does not support this feature
        return "", False
    
    def getServiceGitWorkflow(self, appID, serviceName):
        # The current version does not support this feature
        return "", False
    
    def getServiceDockerImage(self, appID, serviceName):
        # The current version does not support this feature
        return "", False
    
    def getServiceDockerGroup(self, appID, serviceName):
        # The current version does not support this feature
        return "", False
    
    def getServiceDockerName(self, appID, serviceName):
        # The current version does not support this feature
        return "", False
