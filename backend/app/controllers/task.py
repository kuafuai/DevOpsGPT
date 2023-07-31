from flask import Blueprint, request, session
from app.controllers.common import json_response
from app.models.task import getTaskInfo, getEmptyTaskInfo
from app.pkgs.tools.i18b import getI18n
from config import GRADE

bp = Blueprint('task', __name__, url_prefix='/task')

@bp.route('/clear_up', methods=['GET'])
@json_response
def clear_up(): 
    try:
        session.pop(session["username"])
    except Exception as e:
        print("clear_up failed:"+str(e))
    
    session[session["username"]] = getEmptyTaskInfo()
    session.update()

    return {"username": session["username"], "info": session[session["username"]]} 


@bp.route('/setup_app', methods=['POST'])
@json_response
def setup_app():
    _ = getI18n("controllers")
    data = request.json
    appName = data['app_name']
    appId = data['app_id']
    appIntro = data['app_intro']
    repoList = data['repo_list']
    apiDocUrl = data["api_doc_url"]
    sourceBranch = data['source_branch']
    featureBranch = data['feature_branch']
    username = session['username']

    session[username]['memory']['appconfig'], success = getTaskInfo(username, appName, appId,
                                                                    appIntro,  repoList, apiDocUrl,
                                                                    sourceBranch, featureBranch)
    session.update()

    if success:
        # the base version does not split the service
        if GRADE == "base":
            repoList = [session[username]['memory']['appconfig']['taskID']]
        return {"app_name": appName, 
                "repo_list": repoList,
                "source_branch": sourceBranch,
                "feature_branch": featureBranch,
                "task_id": session[username]['memory']['appconfig']['taskID']}
    else:
        raise Exception(_("Failed to set up app."))
