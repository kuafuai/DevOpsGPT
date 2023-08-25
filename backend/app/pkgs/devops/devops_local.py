from app.pkgs.devops.devops_interface import DevopsInterface
from config import WORKSPACE_PATH

class DevopsLocal(DevopsInterface):
    def triggerPipeline(self, branch_name, serviceInfo, ciConfigList):
        return "The pipeline cannot be run locally now, you can view the configuration and select tools such as gitlab.", 0, "", False
    
    def getPipelineStatus(self, pipline_id, repopath, ciConfigList):
        return "The pipeline cannot be run locally now, you can view the configuration and select tools such as gitlab.", 0, "", False
    
    def getPipelineJobLogs(self, repopath, pipeline_id, job_id, ciConfigList):
        return "The pipeline cannot be run locally now, you can view the configuration and select tools such as gitlab.", 0, "", False