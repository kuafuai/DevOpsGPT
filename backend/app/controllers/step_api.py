from flask import request
from app.pkgs.tools import storage
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
    username = storage.get("username")
    requirementID = request.json.get('task_id')
    tenant_id = storage.get("tenant_id")

    # todo Use llm to determine which interface documents to adjust
    req = Requirement.get_requirement_by_id(requirementID, tenant_id)
    apiDoc, success = getServiceSwagger(req["app_id"], 0)

    Requirement.update_requirement(requirement_id=requirementID, tenant_id=tenant_id, original_requirement=userPrompt)

    msg, success = clarifyAPI(requirementID, userPrompt, apiDoc)

    if success:
        return {'message': msg}
    else:
        raise Exception(_("Failed to clarify API."))