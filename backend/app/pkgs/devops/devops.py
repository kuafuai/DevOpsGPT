from app.pkgs.devops.devops_gitlab import DevopsGitlab
from app.pkgs.devops.devops_local import DevopsLocal
from app.pkgs.devops.devops_github import DevopsGitHub
from app.pkgs.devops.devops_pro import triggerPipelinePro
from config import GRADE

def triggerPipeline(requirementID, branchName, serviceInfo, ciConfig):
    DEVOPS_TOOLS = ciConfig["ci_provider"]

    if DEVOPS_TOOLS == 'local':
        obj = DevopsLocal()
    elif DEVOPS_TOOLS == 'gitlab' or DEVOPS_TOOLS ==  'GitLab':
        obj = DevopsGitlab()
    elif DEVOPS_TOOLS == 'github' or DEVOPS_TOOLS ==  'GitHub':
        obj = DevopsGitHub()

    result, piplineID, piplineUrl, success = obj.triggerPipeline(branchName, serviceInfo, ciConfig)

    if GRADE != "base":
        triggerPipelinePro(requirementID, branchName, {"piplineUrl": piplineUrl, "piplineID": piplineID, "repopath": serviceInfo["git_path"]}, ciConfig)
    
    return result, piplineID, piplineUrl, success

def getPipelineStatus(piplineId, repoPath, ciConfig):
    DEVOPS_TOOLS = ciConfig["ci_provider"]

    if DEVOPS_TOOLS == 'local':
        obj = DevopsLocal()
    elif DEVOPS_TOOLS == 'gitlab' or DEVOPS_TOOLS ==  'GitLab':
        obj = DevopsGitlab()
    elif DEVOPS_TOOLS == 'github' or DEVOPS_TOOLS ==  'GitHub':
        obj = DevopsGitHub()
    
    return obj.getPipelineStatus(piplineId, repoPath, ciConfig)

def getPipelineJobLogs(repopath, pipeline_id, job_id, ciConfig):
    DEVOPS_TOOLS = ciConfig["ci_provider"]

    if DEVOPS_TOOLS == 'local':
        obj = DevopsLocal()
    elif DEVOPS_TOOLS == 'gitlab' or DEVOPS_TOOLS ==  'GitLab':
        obj = DevopsGitlab()
    elif DEVOPS_TOOLS == 'github' or DEVOPS_TOOLS ==  'GitHub':
        obj = DevopsGitHub()
    
    return obj.getPipelineJobLogs(obj, repopath, pipeline_id, job_id, ciConfig)