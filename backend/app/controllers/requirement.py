from flask import Blueprint, request, session
from app.controllers.common import json_response
from app.models.task import getEmptyTaskInfo
from app.pkgs.tools.i18b import getI18n
from app.models.requirement import Requirement
from config import REQUIREMENT_STATUS_NotStarted

bp = Blueprint('requirement', __name__, url_prefix='/requirement')

@bp.route('/clear_up', methods=['GET'])
@json_response
def clear_up(): 
    try:
        session.pop(session["username"])
    except Exception as e:
        print("clear_up failed:"+str(e))
    
    session[session["username"]] = getEmptyTaskInfo()
    # todo 1
    session['tenant_id'] = 0
    session.update()

    return {"username": session["username"], "info": session[session["username"]]} 


@bp.route('/setup_app', methods=['POST'])
@json_response
def setup_app():
    _ = getI18n("controllers")
    data = request.json
    appID = data['app_id']
    sourceBranch = data['source_branch']
    featureBranch = data['feature_branch']
    username = session['username']

    requirement = Requirement.create_requirement("", "New", appID, 1, sourceBranch, featureBranch,  REQUIREMENT_STATUS_NotStarted, 0, 0)

    session[username]['memory']['task_info'] = {
        "app_id": appID,
        "task_id": requirement.requirement_id,
        "source_branch": sourceBranch,
        "feature_branch": featureBranch
    }
    session.update()

    if requirement.requirement_id:
        return {"task_id": session[username]['memory']['task_info']['task_id']}
    else:
        raise Exception(_("Failed to set up app."))

@bp.route('/get', methods=['GET'])
@json_response
def getAll():
    _ = getI18n("controllers")
    owner = session['username']
    appID = request.args.get('app_id')

    try:
        requirements = Requirement.get_all_requirements(appID)

        return {'requirements': requirements}
    except Exception as e:
        raise Exception(_("Failed to get applications.")) 