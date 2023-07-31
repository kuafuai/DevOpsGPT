from app.pkgs.devops.devops_gitlab import DevopsGitlab
from app.pkgs.devops.devops_local import DevopsLocal
from config import DEVOPS_TOOLS

def triggerPipeline(filePath, branchName, repoPath):
    if DEVOPS_TOOLS == 'local':
        obj = DevopsLocal()
    elif DEVOPS_TOOLS == 'gitlab':
        obj = DevopsGitlab()
    
    return obj.triggerPipeline(obj, filePath, branchName, repoPath)

def getPipelineStatus(piplineId, repoPath):
    if DEVOPS_TOOLS == 'local':
        obj = DevopsLocal()
    elif DEVOPS_TOOLS == 'gitlab':
        obj = DevopsGitlab()
    
    return obj.getPipelineStatus(piplineId, repoPath)

def getPipelineJobLogs(repopath, pipeline_id, job_id):
    if DEVOPS_TOOLS == 'local':
        obj = DevopsLocal()
    elif DEVOPS_TOOLS == 'gitlab':
        obj = DevopsGitlab()
    
    return obj.getPipelineJobLogs(obj, repopath, pipeline_id, job_id)