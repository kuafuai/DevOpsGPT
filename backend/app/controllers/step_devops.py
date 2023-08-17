from flask import request, session
from app.controllers.common import json_response
from app.pkgs.prompt.prompt import aiAnalyzeError
from app.pkgs.devops.local_tools import compileCheck, lintCheck
from app.pkgs.tools.i18b import getI18n
from app.pkgs.devops.devops import triggerPipeline, getPipelineStatus
from app.pkgs.knowledge.app_info import getServiceGitPath, getServiceGitWorkflow, getServiceDockerImage, getServiceDockerGroup, getServiceDockerName
from app.pkgs.tools.file_tool import get_ws_path
from app.pkgs.devops.cd import triggerCD
from config import WORKSPACE_PATH
from flask import Blueprint

bp = Blueprint('step_devops', __name__, url_prefix='/step_devops')

@bp.route('/trigger_ci', methods=['POST'])
@json_response
def trigger_ci():
    serviceName = request.json.get('repo_path')
    username = session['username']
    appID = session[username]['memory']['task_info']['app_id']
    gitPath, success = getServiceGitPath(appID, serviceName)
    gitWorkflow, success = getServiceGitWorkflow(appID, serviceName)

    username = session['username']
    branch = session[username]['memory']['task_info']['feature_branch']

    result, piplineID, piplineUrl, success = triggerPipeline(branch, gitPath, gitWorkflow)
    if success:
        return {"name": 'ci', "info": {"piplineID": piplineID, "repopath": gitPath, "piplineUrl": piplineUrl}}
    else:
        raise Exception(result)


@bp.route('/plugin_ci', methods=['GET'])
@json_response
def plugin_ci():
    pipeline_id = request.args.get('piplineID')
    repopath = request.args.get('repopath')

    piplineJobs, success = getPipelineStatus(pipeline_id, repopath)
    print("piplineJobs:", piplineJobs)

    if success:
        return {'piplineJobs': piplineJobs}
    else:
        raise Exception(piplineJobs)
    


@bp.route('/check_compile', methods=['POST'])
@json_response
def check_compile():
    _ = getI18n("controllers")
    task_id = session[session['username']]['memory']['task_info']['task_id']
    serviceName = request.json.get('repo_path')
    wsPath = get_ws_path(task_id)
    username = session['username']
    appID = session[username]['memory']['task_info']['app_id']
    gitPath, success = getServiceGitPath(appID, serviceName)

    success, message = compileCheck(wsPath, gitPath)

    if success:
        reasoning = _("Compile check pass.")
        return {'pass': True, 'message': message, 'reasoning': reasoning}
    else:
        reasoning, success = aiAnalyzeError(message)
        if success:
            return {'pass': False, 'message': message, 'reasoning': reasoning}
        else:
            raise Exception(_("Compile check failed for unknown reasons."))


@bp.route('/check_lint', methods=['POST'])
@json_response
def check_lint():
    _ = getI18n("controllers")
    task_id = session[session['username']]['memory']['task_info']['task_id']
    file_path = request.json.get('file_path')
    serviceName = request.json.get('service_name')
    username = session['username']
    appID = session[username]['memory']['task_info']['app_id']
    gitPath, success = getServiceGitPath(appID, serviceName)
    ws_path = get_ws_path(task_id)

    success, message = lintCheck(ws_path, gitPath, file_path)

    if success:
        reasoning = _("Static code scan passed.")
        return {'pass': True, 'message': message, 'reasoning': reasoning}
    else:
        reasoning, success = aiAnalyzeError(message)
        if success:
            return {'pass': False, 'message': message, 'reasoning': reasoning}
        else:
            raise Exception(_("Static code scan failed for unknown reasons."))

@bp.route('/trigger_cd', methods=['POST'])
@json_response
def trigger_cd():
    username = session['username']
    appID = session[username]['memory']['task_info']['app_id']
    serviceName = request.json.get('repo_path')
    image, success = getServiceDockerImage(appID, serviceName)
    dockerGroup, success = getServiceDockerGroup(appID, serviceName)
    dockerName, success = getServiceDockerName(appID, serviceName)

    result, success = triggerCD(image, dockerGroup, dockerName)
    if success:
        return {"internet_ip": result}
    else:
        raise Exception(result)