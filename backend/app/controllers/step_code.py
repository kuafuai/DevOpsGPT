from flask import request
from app.pkgs.tools import storage
from app.controllers.common import json_response
from app.pkgs.tools.i18b import getI18n
from app.pkgs.prompt.prompt import aiGenCode, aiMergeCode, aiCheckCode, aiFixError, aiReferenceRepair
from app.pkgs.devops.local_tools import getFileContent
from flask import Blueprint

from app.pkgs.prompt.prompt import gen_write_code

bp = Blueprint('step_code', __name__, url_prefix='/step_code')

@bp.route('/edit_file_task', methods=['POST'])
@json_response
def edit_file_task():
    _ = getI18n("controllers")
    newTask = request.json.get('new_task')
    newCode = request.json.get('new_code')
    fileTask = request.json.get('file_task')
    filePath = request.json.get('file_path')
    requirementID = request.json.get('task_id')

    re, success = aiGenCode(requirementID, fileTask, newTask, newCode, filePath)
    if not success:
        raise Exception(_("Failed to edit file with new task."))

    return {'success': success, 'code': re["code"], 'reasoning': re["reasoning"]}

@bp.route('/check_code', methods=['POST'])
@json_response
def check_file():
    _ = getI18n("controllers")
    code = request.json.get('code')
    fileTask = request.json.get('fileTask')
    requirementID = request.json.get('task_id')
    filePath = request.json.get('file_path')
    step = request.json.get('step')
    service_name = request.json.get('service_name')
    
    if step:
        re, success = gen_write_code(requirementID, service_name, filePath, fileTask, step)
    else:
        re, success = aiCheckCode(requirementID, fileTask, code, filePath, service_name)
    if not success:
        raise Exception(_("Failed to check file."))

    return {'success': success, 'code': re["code"], 'reasoning': re["reasoning"]}

@bp.route('/merge_file', methods=['POST'])
@json_response
def merge_file():
    _ = getI18n("controllers")
    baseCode = request.json.get('old_code')
    newCode = request.json.get('new_code')
    fileTask = request.json.get('file_task')
    userName = storage.get("username")
    requirementID = request.json.get('task_id')
    filePath = request.json.get('file_path')

    re, success = aiMergeCode(requirementID, fileTask, baseCode, newCode, filePath)
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
    userName = storage.get("username")
    requirementID = request.json.get('task_id')
    filePath = request.json.get('file_path')

    hasGitCode, referenceCode =  getFileContent(referenceFile, repo)
    if not hasGitCode:
        raise Exception(_("Failed to reference repair no reference file found."))

    re, success = aiReferenceRepair(requirementID, newCode, referenceCode, fileTask, filePath)
    if not success:
        raise Exception(_("Reference repair failed for unknown reasons."))

    return {'success': success, 'code': re["code"], 'reasoning': re["reasoning"]}


@bp.route('/fix_compile', methods=['POST'])
@json_response
def fix_compile():
    code = request.json.get('code')
    solution = request.json.get('solution')
    requirementID = request.json.get('task_id')
    filePath = request.json.get('file_path')
    error_msg = request.json.get('error_msg')

    re, success = aiFixError(requirementID, error_msg, solution, code, filePath, "compile")
    reCode = re["code"]
    reason = re["reasoning"]

    return {'success': success, 'code': reCode, 'reasoning': reason}


@bp.route('/fix_lint', methods=['POST'])
@json_response
def fix_lint():
    code = request.json.get('code')
    solution = request.json.get('solution')
    requirementID = request.json.get('task_id')
    filePath = request.json.get('file_path')
    error_msg = request.json.get('error_msg')

    re, success = aiFixError(requirementID ,error_msg, solution, code, filePath, "lint")
    reCode = re["code"]
    reason = re["reasoning"]

    return {'success': success, 'code': reCode, 'reasoning': reason}