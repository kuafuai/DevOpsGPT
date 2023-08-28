from flask import request, session
from app.controllers.common import json_response
from flask import Blueprint
from app.pkgs.tools.i18b import getI18n
from app.pkgs.prompt.prompt import clarifyAPI
from app.pkgs.knowledge.app_info import getServiceSwagger
from app.models.requirement import Requirement

bp = Blueprint('step_api', __name__, url_prefix='/step_api')

@bp.route('/clarify', methods=['POST'])
@json_response
def gen_interface_doc():
    _ = getI18n("controllers")
    userPrompt = request.json.get('user_prompt')
    username = session["username"]
    requirementID = request.json.get('task_id')

    # todo Use llm to determine which interface documents to adjust
    req = Requirement.get_requirement_by_id(requirementID)
    apiDoc, success = getServiceSwagger(req["app_id"], 0)

    msg, success = clarifyAPI(requirementID, userPrompt, apiDoc)

    session[username]['memory']['originalPrompt'] = userPrompt
    session.update()

    if success:
        return {'message': msg}
    else:
        raise Exception(_("Failed to clarify API."))