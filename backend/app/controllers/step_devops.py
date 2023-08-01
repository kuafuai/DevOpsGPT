from flask import request, session
from app.controllers.common import json_response
from app.pkgs.prompt.prompt import aiAnalyzeError
from app.pkgs.devops.local_tools import compileCheck, lintCheck
from app.pkgs.tools.i18b import getI18n
from app.pkgs.devops.devops import triggerPipeline, getPipelineStatus
from config import WORKSPACE_PATH
from flask import Blueprint

bp = Blueprint('step_devops', __name__, url_prefix='/step_devops')

@bp.route('/trigger_ci', methods=['POST'])
@json_response
def trigger_ci():
    repo_path = request.json.get('repo_path')

    username = session['username']
    branch = session[username]['memory']['appconfig']['featureBranch']

    result, piplineID, piplineUrl, success = triggerPipeline(branch, repo_path)
    if success:
        return {"name": 'ci', "info": {"piplineID": piplineID, "repopath": repo_path, "piplineUrl": piplineUrl}}
    else:
        raise Exception(result)


@bp.route('/plugin_ci', methods=['GET'])
@json_response
def plugin_ci():
    pipeline_id = request.args.get('piplineID')
    repopath = request.args.get('repopath')

    piplineJobs = getPipelineStatus(pipeline_id, repopath)
    print("piplineJobs:", piplineJobs)

    return {'piplineJobs': piplineJobs}


@bp.route('/check_compile', methods=['POST'])
@json_response
def check_compile():
    _ = getI18n("controllers")
    task_id = session[session['username']]['memory']['appconfig']['taskID']
    repo_path = request.json.get('repo_path')
    ws_path = WORKSPACE_PATH+task_id+'/'+repo_path

    success, message = compileCheck(ws_path, repo_path)

    if success:
        reasoning = _("Compile check pass.")
        return {'pass': True, 'message': message, 'reasoning': reasoning}
    else:
        reasoning, success = aiAnalyzeError(message)
        if success:
            return {'pass': False, 'message': message, 'reasoning': reasoning}
        else:
            raise Exception(_("Compile check failed for unknown reasons."))


@bp.route('/check_lint', methods=['POST'])
@json_response
def check_lint():
    _ = getI18n("controllers")
    task_id = session[session['username']]['memory']['appconfig']['taskID']
    file_path = request.json.get('file_path')
    repo_path = request.json.get('service_name')
    ws_path = WORKSPACE_PATH+task_id+'/'+repo_path

    success, message = lintCheck(ws_path, repo_path, file_path)

    if success:
        reasoning = _("Static code scan passed.")
        return {'pass': True, 'message': message, 'reasoning': reasoning}
    else:
        reasoning, success = aiAnalyzeError(message)
        if success:
            return {'pass': False, 'message': message, 'reasoning': reasoning}
        else:
            raise Exception(_("Static code scan failed for unknown reasons."))
