from flask import request, session
from app.controllers.common import json_response
from flask import Blueprint
from app.pkgs.tools.i18b import getI18n
from app.pkgs.prompt.prompt import clarifyRequirement
from app.pkgs.knowledge.app_info import getAppArchitecture
from app.models.requirement import Requirement
from config import REQUIREMENT_STATUS_InProgress

bp = Blueprint('step_requirement', __name__, url_prefix='/step_requirement')

@bp.route('/clarify', methods=['POST'])
@json_response
def clarify():
    _ = getI18n("controllers")
    userPrompt = request.json.get('user_prompt')
    globalContext = request.json.get('global_context')
    userName = session["username"]
    requirementID = request.json.get('task_id')

    req = Requirement.get_requirement_by_id(requirementID) 

    if not req["app_id"] or req["app_id"] < 1 :
        raise Exception(_("Please select the application you want to develop."))
    
    if len(globalContext) < 4 :
        Requirement.update_requirement(requirement_id=requirementID, original_requirement=userPrompt, status=REQUIREMENT_STATUS_InProgress)
    
    appArchitecture, _ = getAppArchitecture(req["app_id"])
    msg, success = clarifyRequirement(requirementID, userPrompt, globalContext, appArchitecture)

    if success:
        return {'message': msg, 'memory': session[userName]['memory']}
    else:
        raise Exception(_("Failed to clarify requirement."))
