from flask import request, session
from app.controllers.common import json_response
from flask import Blueprint
from app.pkgs.tools.i18b import getI18n
from app.pkgs.prompt.prompt import clarifyRequirement

bp = Blueprint('step_requirement', __name__, url_prefix='/step_requirement')

@bp.route('/clarify', methods=['POST'])
@json_response
def clarify():
    _ = getI18n("controllers")
    userPrompt = request.json.get('user_prompt')
    globalContext = request.json.get('global_context')
    userName = session["username"]

    appName = session[userName]['memory']['appconfig']['appName']
    if len(appName) == 0:
        raise Exception(_("Please select the application you want to develop."))
            
    msg, success = clarifyRequirement(userPrompt, globalContext)

    if success:
        return {'message': msg, 'memory': session[userName]['memory']}
    else:
        raise Exception(_("Failed to clarify requirement."))
