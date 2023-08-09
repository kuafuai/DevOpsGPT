from app.pkgs.devops.devops_gitlab import DevopsGitlab
from app.pkgs.devops.devops_local import DevopsLocal
from app.pkgs.devops.devops_github import DevopsGitHub
from config import DEVOPS_TOOLS

def triggerPipeline(branchName, repoPath, gitWorkflow):
    if DEVOPS_TOOLS == 'local':
        obj = DevopsLocal()
    elif DEVOPS_TOOLS == 'gitlab':
        obj = DevopsGitlab()
    elif DEVOPS_TOOLS == 'github':
        obj = DevopsGitHub()
    
    return obj.triggerPipeline(branchName, repoPath, gitWorkflow)

def getPipelineStatus(piplineId, repoPath):
    if DEVOPS_TOOLS == 'local':
        obj = DevopsLocal()
    elif DEVOPS_TOOLS == 'gitlab':
        obj = DevopsGitlab()
    elif DEVOPS_TOOLS == 'github':
        obj = DevopsGitHub()
    
    return obj.getPipelineStatus(piplineId, repoPath)

def getPipelineJobLogs(repopath, pipeline_id, job_id):
    if DEVOPS_TOOLS == 'local':
        obj = DevopsLocal()
    elif DEVOPS_TOOLS == 'gitlab':
        obj = DevopsGitlab()
    elif DEVOPS_TOOLS == 'github':
        obj = DevopsGitHub()
    
    return obj.getPipelineJobLogs(obj, repopath, pipeline_id, job_id)