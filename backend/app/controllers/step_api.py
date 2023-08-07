from flask import request, session
from app.controllers.common import json_response
from flask import Blueprint
from app.pkgs.tools.i18b import getI18n
from app.pkgs.prompt.prompt import clarifyAPI
from app.pkgs.knowledge.app_info import getServiceSwagger

bp = Blueprint('step_api', __name__, url_prefix='/step_api')

@bp.route('/clarify', methods=['POST'])
@json_response
def gen_interface_doc():
    _ = getI18n("controllers")
    userPrompt = request.json.get('user_prompt')
    username = session["username"]

    # todo Use llm to determine which interface documents to adjust
    appID = session[username]['memory']['task_info']['app_id']
    apiDoc, success = getServiceSwagger(appID, 0)

    msg, success = clarifyAPI(userPrompt, apiDoc)

    session[username]['memory']['originalPrompt'] = userPrompt
    session.update()

    if success:
        return {'message': msg}
    else:
        raise Exception(_("Failed to clarify API."))