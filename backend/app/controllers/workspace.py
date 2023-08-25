from flask import request, session
from app.controllers.common import json_response
from app.pkgs.tools.i18b import getI18n
from app.pkgs.devops.git_tools import pullCode, pushCode
from app.pkgs.knowledge.app_info import getServiceGitPath
from app.models.setting import getGitConfigList
from config import GIT_ENABLED
from app.pkgs.tools.file_tool import get_ws_path, write_file_content
from flask import Blueprint

bp = Blueprint('workspace', __name__, url_prefix='/workspace')

@bp.route('/save_code', methods=['POST'])
@json_response
def save_code():
    _ = getI18n("controllers")
    task_id = request.json.get('task_id')
    file_path = request.json.get('file_path')
    serviceName = request.json.get('service_name')
    code = request.json.get('code')
    username = session['username']
    appID = session[username]['memory']['task_info']['app_id']
    gitPath, success = getServiceGitPath(appID, serviceName)
    path = get_ws_path(task_id)+'/'+gitPath+"/"+file_path
    write_file_content(path, code)
    return _("Saved code successfully.")


@bp.route('/create', methods=['POST'])
@json_response
def create():
    _ = getI18n("controllers")
    task_id =  request.json.get('task_id')
    serviceName = request.json.get('repo_path')
    base_branch = request.json.get('base_branch')
    fature_branch = request.json.get('feature_branch')
    ws_path = get_ws_path(task_id)
    username = session['username']
    appID = session[username]['memory']['task_info']['app_id']
    print(appID)
    print("@@@@@@@@")
    gitPath, success = getServiceGitPath(appID, serviceName)

    tenantID = session['tenant_id']
    username = session['username']
    appID = session[username]['memory']['task_info']['app_id']
    gitConfigList, success = getGitConfigList(tenantID, appID)

    if not GIT_ENABLED:
        success = True
    else:
        success, msg = pullCode(ws_path, gitPath, base_branch, fature_branch, gitConfigList)

    if success:
        return _("Create workspace successfully.")
    else:
        raise Exception(_("Failed to create workspace.")+f"In the {ws_path}/{gitPath} directory, {msg}")

@bp.route('/gitpush', methods=['POST'])
@json_response
def gitpush():
    _ = getI18n("controllers")
    username = session['username']
    commitMsg = session[username]['memory']['originalPrompt']
    task_id =  request.json.get('task_id')
    serviceName = request.json.get('service_name')
    fatureBranch = session[username]['memory']['task_info']['feature_branch']
    wsPath = get_ws_path(task_id)
    appID = session[username]['memory']['task_info']['app_id']
    gitPath, success = getServiceGitPath(appID, serviceName)
    tenantID = session['tenant_id']
    username = session['username']
    appID = session[username]['memory']['task_info']['app_id']
    gitConfigList, success = getGitConfigList(tenantID, appID)

    if not GIT_ENABLED:
        raise Exception(_("Failed to push code.")+f" You did not set Git parameters in the configuration file.")
    else:
        success, msg = pushCode(wsPath, gitPath, fatureBranch, commitMsg, gitConfigList)

    if success:
        return _("Push code successfully.") + f" from {wsPath} to {gitPath} {fatureBranch}"
    else:
        raise Exception(_("Failed to push code.")+f"In the {wsPath}/{gitPath} directory, {msg}")
