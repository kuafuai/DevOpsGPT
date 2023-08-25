from app.pkgs.devops.devops_gitlab import DevopsGitlab
from app.pkgs.devops.devops_local import DevopsLocal
from app.pkgs.devops.devops_github import DevopsGitHub

def triggerPipeline(branchName, serviceInfo, ciConfig):
    DEVOPS_TOOLS = ciConfig["ci_provider"]

    if DEVOPS_TOOLS == 'local':
        obj = DevopsLocal()
    elif DEVOPS_TOOLS == 'gitlab':
        obj = DevopsGitlab()
    elif DEVOPS_TOOLS == 'github':
        obj = DevopsGitHub()
    
    return obj.triggerPipeline(branchName, serviceInfo, ciConfig)

def getPipelineStatus(piplineId, repoPath, ciConfig):
    DEVOPS_TOOLS = ciConfig["ci_provider"]

    if DEVOPS_TOOLS == 'local':
        obj = DevopsLocal()
    elif DEVOPS_TOOLS == 'gitlab':
        obj = DevopsGitlab()
    elif DEVOPS_TOOLS == 'github':
        obj = DevopsGitHub()
    
    return obj.getPipelineStatus(piplineId, repoPath, ciConfig)

def getPipelineJobLogs(repopath, pipeline_id, job_id, ciConfig):
    DEVOPS_TOOLS = ciConfig["ci_provider"]

    if DEVOPS_TOOLS == 'local':
        obj = DevopsLocal()
    elif DEVOPS_TOOLS == 'gitlab':
        obj = DevopsGitlab()
    elif DEVOPS_TOOLS == 'github':
        obj = DevopsGitHub()
    
    return obj.getPipelineJobLogs(obj, repopath, pipeline_id, job_id, ciConfig)