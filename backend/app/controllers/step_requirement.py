from flask import request, session
from app.controllers.common import json_response
from flask import Blueprint
from app.pkgs.prompt.requirement import clarifyRequirement
from app.pkgs.prompt.requirement_pro import clarifyRequirementPro
from app.pkgs.tools.i18b import getI18n
from config import GRADE

bp = Blueprint('step_requirement', __name__, url_prefix='/step_requirement')

@bp.route('/clarify', methods=['POST'])
@json_response
def clarify():
    _ = getI18n("controllers")
    user_prompt = request.json.get('user_prompt')
    global_context = request.json.get('global_context')
    userName = session["username"]

    appName = session[userName]['memory']['appconfig']['appName']
    if len(appName) == 0:
        raise Exception(_("Please select the application you want to develop."))

    if GRADE == "base":
        msg, success = clarifyRequirement(user_prompt, global_context, appName)
    else:
        msg, success = clarifyRequirementPro(user_prompt, global_context, appName)

    if success:
        return {'message': msg, 'memory': session[userName]['memory']}
    else:
        raise Exception(_("Failed to clarify requirement."))
