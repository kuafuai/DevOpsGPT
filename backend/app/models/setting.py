from app.models.setting_basic import SettingBasic
from app.models.setting_pro import SettingPro
from config import GRADE


def getGitConfigList(tenantID, appID, hideToken=True):
    if GRADE == "base":
        obj = SettingBasic()
    else:
        obj = SettingPro()
        
    return obj.getGitConfigList(tenantID, appID, hideToken=hideToken)

def getCIConfigList(tenantID, appID, hideToken=True):
    if GRADE == "base":
        obj = SettingBasic()
    else:
        obj = SettingPro()
        
    return obj.getCIConfigList(tenantID, appID, hideToken=hideToken)

def getCDConfigList(tenantID, appID, hideToken=True):
    if GRADE == "base":
        obj = SettingBasic()
    else:
        obj = SettingPro()
        
    return obj.getCDConfigList(tenantID, appID, hideToken=hideToken)

def getLLMConfigList(tenantID, appID):
    if GRADE == "base":
        obj = SettingBasic()
    else:
        obj = SettingPro()
        
    return obj.getLLMConfigList(tenantID, appID)