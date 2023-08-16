from app.pkgs.devops.cd_aliyun import CDAliyun
from app.pkgs.devops.cd_local import CDLocal
from config import CD_TOOLS

def triggerCD(image, container_grpup, container_name):
    if CD_TOOLS == 'local':
        obj = CDLocal()
    elif CD_TOOLS == 'aliyun':
        obj = CDAliyun()
    
    return obj.triggerCD(image, container_grpup, container_name)