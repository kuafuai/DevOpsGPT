from app.pkgs.devops.cd_aliyun import CDAliyun
from app.pkgs.devops.cd_local import CDLocal

def triggerCD(image, serviceInfo, cdConfig):
    CD_TOOLS = cdConfig["cd_provider"]

    if CD_TOOLS == 'local':
        obj = CDLocal()
    elif CD_TOOLS == 'aliyun':
        obj = CDAliyun()
    
    return obj.triggerCD(image, serviceInfo, cdConfig)