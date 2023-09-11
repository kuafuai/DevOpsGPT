from flask import request, session
from app.controllers.common import json_response
from app.pkgs.tools.i18b import getI18n
from app.pkgs.devops.git_tools import pullCode, pushCode, gitResetWorkspace
from app.pkgs.knowledge.app_info import getServiceGitPath
from app.models.setting import getGitConfigList
from app.models.requirement import Requirement
from config import REQUIREMENT_STATUS_Completed
from config import GIT_ENABLED
from app.pkgs.tools.file_tool import get_ws_path, write_file_content
from flask import Blueprint

bp = Blueprint('workspace', __name__, url_prefix='/workspace')

@bp.route('/save_code', methods=['POST'])
@json_response
def save_code():
    _ = getI18n("controllers")
    requirementID = request.json.get('task_id')
    file_path = request.json.get('file_path')
    serviceName = request.json.get('service_name')
    code = request.json.get('code')
    req = Requirement.get_requirement_by_id(requirementID) 
    gitPath, success = getServiceGitPath(req["app_id"] , serviceName)
    path = get_ws_path(requirementID)+'/'+gitPath+"/"+file_path
    write_file_content(path, code)
    return _("Saved code successfully.")


@bp.route('/create', methods=['POST'])
@json_response
def create():
    _ = getI18n("controllers")
    requirementID =  request.json.get('task_id')
    serviceName = request.json.get('repo_path')
    ws_path = get_ws_path(requirementID)
    req = Requirement.get_requirement_by_id(requirementID) 
    
    gitPath, success = getServiceGitPath(req["app_id"], serviceName)

    tenantID = session['tenant_id']
    gitConfigList, success = getGitConfigList(tenantID, req["app_id"])

    if not GIT_ENABLED:
        success = True
    else:
        success, msg = pullCode(ws_path, gitPath, req["default_source_branch"], req["default_target_branch"], gitConfigList)

    if success:
        return _("Create workspace successfully.")
    else:
        raise Exception(_("Failed to create workspace.")+f"In the {ws_path}/{gitPath} directory, {msg}")

@bp.route('/gitpush', methods=['POST'])
@json_response
def gitpush():
    _ = getI18n("controllers")
    username = session['username']
    requirementID =  request.json.get('task_id')
    serviceName = request.json.get('service_name')
    wsPath = get_ws_path(requirementID)
    req = Requirement.get_requirement_by_id(requirementID) 
    commitMsg = req["requirement_name"]
    fatureBranch = req["default_target_branch"]
    gitPath, success = getServiceGitPath(req["app_id"], serviceName)
    tenantID = session['tenant_id']
    username = session['username']
    gitConfigList, success = getGitConfigList(tenantID, req["app_id"])

    Requirement.update_requirement(requirement_id=requirementID, status=REQUIREMENT_STATUS_Completed)

    if not GIT_ENABLED:
        raise Exception(_("Failed to push code.")+f" You did not set Git parameters in the configuration file.")
    else:
        success, msg = pushCode(wsPath, gitPath, fatureBranch, commitMsg, gitConfigList)

    if success:
        return _("Push code successfully.") + f" from {wsPath} to {gitPath} {fatureBranch}"
    else:
        raise Exception(_("Failed to push code.")+f"In the {wsPath}/{gitPath} directory, {msg}")


@bp.route('/resetWorkspace', methods=['POST'])
@json_response
def resetWorkspace():
    _ = getI18n("controllers")
    username = session['username']
    requirementID =  request.json.get('task_id')
    serviceName = request.json.get('service_name')
    wsPath = get_ws_path(requirementID)
    req = Requirement.get_requirement_by_id(requirementID) 
    commitMsg = req["requirement_name"]
    fatureBranch = req["default_target_branch"]
    gitPath, success = getServiceGitPath(req["app_id"], serviceName)
    tenantID = session['tenant_id']
    username = session['username']
    gitConfigList, success = getGitConfigList(tenantID, req["app_id"])

    Requirement.update_requirement(requirement_id=requirementID, status=REQUIREMENT_STATUS_Completed)

    if not GIT_ENABLED:
        raise Exception(_("Failed to reset code.")+f" You did not set Git parameters in the configuration file.")
    else:
        success, msg = gitResetWorkspace(wsPath, gitPath, fatureBranch, commitMsg, gitConfigList)

    if success:
        return True
    else:
        raise Exception(_("Failed to reset code.")+f"In the {wsPath}/{gitPath} directory, {msg}")