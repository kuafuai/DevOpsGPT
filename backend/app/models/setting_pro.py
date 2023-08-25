from app.models.setting_interface import SettingInterface

class SettingPro(SettingInterface):
    def getGitConfigList(self, tenantID, appID):
        # The current version does not support this feature
        return "", False
    
    def getCIConfigList(self, tenantID, appID):
        # The current version does not support this feature
        return "", False
    
    def getCDConfigList(self, tenantID, appID):
        # The current version does not support this feature
        return "", False
    
    def getLLMConfigList(self, tenantID, appID):
        # The current version does not support this feature
        return "", False