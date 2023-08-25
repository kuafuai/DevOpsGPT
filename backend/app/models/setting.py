from app.models.setting_basic import SettingBasic
from app.models.setting_pro import SettingPro
from config import GRADE


def getGitConfigList(tenantID, appID):
    if GRADE == "base":
        obj = SettingBasic()
    else:
        obj = SettingPro()
        
    return obj.getGitConfigList(tenantID, appID)

def getCIConfigList(tenantID, appID):
    if GRADE == "base":
        obj = SettingBasic()
    else:
        obj = SettingPro()
        
    return obj.getCIConfigList(tenantID, appID)

def getCDConfigList(tenantID, appID):
    if GRADE == "base":
        obj = SettingBasic()
    else:
        obj = SettingPro()
        
    return obj.getCDConfigList(tenantID, appID)

def getLLMConfigList(tenantID, appID):
    if GRADE == "base":
        obj = SettingBasic()
    else:
        obj = SettingPro()
        
    return obj.getLLMConfigList(tenantID, appID)