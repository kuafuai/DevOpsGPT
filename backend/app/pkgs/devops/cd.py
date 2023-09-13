from app.pkgs.devops.cd_aliyun import CDAliyun
from app.pkgs.devops.cd_local import CDLocal
from app.pkgs.devops.devops_pro import triggerCDPro
from config import GRADE

def triggerCD(requirementID, image, serviceInfo, cdConfig):
    CD_TOOLS = cdConfig["cd_provider"]

    if CD_TOOLS == 'local':
        obj = CDLocal()
    elif CD_TOOLS == 'aliyun':
        obj = CDAliyun()
    
    re, success =  obj.triggerCD(image, serviceInfo, cdConfig)

    if GRADE != "base":
        triggerCDPro(requirementID, image, re, cdConfig)

    return re, success