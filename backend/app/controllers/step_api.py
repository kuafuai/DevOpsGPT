from flask import request, session
from app.controllers.common import json_response
from flask import Blueprint
from app.pkgs.tools.i18b import getI18n
from app.pkgs.prompt.prompt import clarifyAPI

bp = Blueprint('step_api', __name__, url_prefix='/step_api')

@bp.route('/clarify', methods=['POST'])
@json_response
def gen_interface_doc():
    _ = getI18n("controllers")
    userPrompt = request.json.get('user_prompt')
    username = session["username"]
    apiDocUrl = session[username]['memory']['appconfig']['apiDocUrl']

    msg, success = clarifyAPI(userPrompt, apiDocUrl)

    session[username]['memory']['originalPrompt'] = userPrompt
    session.update()

    if success:
        return {'message': msg}
    else:
        raise Exception(_("Failed to clarify API."))