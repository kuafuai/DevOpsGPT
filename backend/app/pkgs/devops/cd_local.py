from app.pkgs.devops.cd_interface import CDInterface
from config import WORKSPACE_PATH

class CDLocal(CDInterface):
    def triggerCD(self, image, container_grpup, container_name):
        return "The pipeline cannot be run locally now, you can view the configuration and select tools such as gitlab.", 0, "", False