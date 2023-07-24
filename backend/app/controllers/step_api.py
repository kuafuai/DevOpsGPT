from flask import request, session
from app.controllers.common import json_response
from flask import Blueprint
from app.pkgs.prompt.api import clarifyAPI
from app.pkgs.prompt.api_pro import clarifyAPIPro
from app.pkgs.tools.i18b import getI18n
from config import GRADE

bp = Blueprint('step_api', __name__, url_prefix='/step_api')

@bp.route('/clarify', methods=['POST'])
@json_response
def gen_interface_doc():
    _ = getI18n("controllers")
    user_prompt = request.json.get('user_prompt')
    username = session["username"]
    apiDocUrl = session[username]['memory']['appconfig']['apiDocUrl']

    if GRADE == "base":
        msg, success = clarifyAPI(user_prompt, apiDocUrl)
    else:
        msg, success = clarifyAPIPro(user_prompt, apiDocUrl)

    session[username]['memory']['originalPrompt'] = user_prompt
    session.update()

    if success:
        return {'message': msg}
    else:
        raise Exception(_("Failed to clarify API."))