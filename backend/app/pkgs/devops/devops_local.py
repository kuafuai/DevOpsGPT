from app.pkgs.devops.devops_interface import DevopsInterface
from config import WORKSPACE_PATH

class DevopsLocal(DevopsInterface):
    def triggerPipeline(self, branch_name, repopath, gitWorkflow):
        return "The pipeline cannot be run locally now, you can view the configuration and select tools such as gitlab.", 0, "", False
    
    def getPipelineStatus(self, pipline_id, repopath):
        return "The pipeline cannot be run locally now, you can view the configuration and select tools such as gitlab.", 0, "", False
    
    def getPipelineJobLogs(self, repopath, pipeline_id, job_id):
        return "The pipeline cannot be run locally now, you can view the configuration and select tools such as gitlab.", 0, "", False