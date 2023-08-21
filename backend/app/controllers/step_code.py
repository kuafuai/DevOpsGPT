from flask import request, session
from app.controllers.common import json_response
from app.pkgs.tools.i18b import getI18n
from app.pkgs.prompt.prompt import aiGenCode, aiMergeCode, aiCheckCode, aiFixError, aiReferenceRepair
from app.pkgs.devops.local_tools import getFileContent
from flask import Blueprint

bp = Blueprint('step_code', __name__, url_prefix='/step_code')

@bp.route('/edit_file_task', methods=['POST'])
@json_response
def edit_file_task():
    _ = getI18n("controllers")
    newTask = request.json.get('new_task')
    newCode = request.json.get('new_code')
    fileTask = request.json.get('file_task')

    re, success = aiGenCode(fileTask, newTask, newCode)
    if not success:
        raise Exception(_("Failed to edit file with new task."))

    return {'success': success, 'code': re["code"], 'reasoning': re["reasoning"]}

@bp.route('/check_file', methods=['POST'])
@json_response
def check_file():
    _ = getI18n("controllers")
    code = request.json.get('code')
    fileTask = request.json.get('fileTask')

    re, success = aiCheckCode(fileTask, code)
    if not success:
        raise Exception(_("Failed to check file."))

    return {'success': success, 'code': re["code"], 'reasoning': re["reasoning"]}

@bp.route('/merge_file', methods=['POST'])
@json_response
def merge_file():
    _ = getI18n("controllers")
    baseCode = request.json.get('base_code')
    newCode = request.json.get('new_code')
    fileTask = request.json.get('file_task')
    userName = session["username"]
    appName = session[userName]['memory']['task_info']['app_name']

    re, success = aiMergeCode(fileTask, appName, baseCode, newCode)
    if not success:
        raise Exception(_("Failed to merge old and new code."))

    return {'success': success, 'code': re["code"], 'reasoning': re["reasoning"]}

@bp.route('/reference_repair', methods=['POST'])
@json_response
def reference_repair():
    _ = getI18n("controllers")
    fileTask = request.json.get('file_task')
    newCode = request.json.get('new_code')
    referenceFile = request.json.get('reference_file')
    repo = request.json.get('repo')
    userName = session["username"]
    appName = session[userName]['memory']['task_info']['app_name']
    branch = session[userName]['memory']['task_info']['source_branch']

    hasGitCode, referenceCode =  getFileContent(referenceFile, branch, repo)
    if not hasGitCode:
        raise Exception(_("Failed to reference repair no reference file found."))

    re, success = aiReferenceRepair(newCode, appName, referenceCode, fileTask)
    if not success:
        raise Exception(_("Reference repair failed for unknown reasons."))

    return {'success': success, 'code': re["code"], 'reasoning': re["reasoning"]}


@bp.route('/fix_compile', methods=['POST'])
@json_response
def fix_compile():
    code = request.json.get('code')
    solution = request.json.get('solution')

    re, success = aiFixError(solution, code)
    reCode = re["code"]
    reason = re["reasoning"]

    return {'success': success, 'code': reCode, 'reasoning': reason}


@bp.route('/fix_lint', methods=['POST'])
@json_response
def fix_lint():
    code = request.json.get('code')
    solution = request.json.get('solution')

    re, success = aiFixError(solution, code)
    reCode = re["code"]
    reason = re["reasoning"]

    return {'success': success, 'code': reCode, 'reasoning': reason}