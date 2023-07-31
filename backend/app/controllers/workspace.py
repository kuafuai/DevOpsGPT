import re
from flask import request, session
from app.controllers.common import json_response
from app.pkgs.tools.i18b import getI18n
from app.pkgs.devops.git_tools import pullCode, createBranch, pushCode
from config import GRADE
from config import WORKSPACE_PATH
from app.pkgs.tools.file_tool import get_ws_path, write_file_content
from flask import Blueprint

bp = Blueprint('workspace', __name__, url_prefix='/workspace')

@bp.route('/save_code', methods=['POST'])
@json_response
def save_code():
    _ = getI18n("controllers")
    task_id = session[session['username']]['memory']['appconfig']['taskID']
    file_path = request.json.get('file_path')
    repo_path = request.json.get('service_name')
    code = request.json.get('code')
    path = WORKSPACE_PATH+task_id+'/'+repo_path+"/"+file_path
    write_file_content(path, code)
    return _("Saved code successfully.")


@bp.route('/create', methods=['POST'])
@json_response
def create():
    _ = getI18n("controllers")
    task_id =  session[session['username']]['memory']['appconfig']['taskID']
    repo_path = request.json.get('repo_path')
    base_branch = request.json.get('base_branch')
    fature_branch = request.json.get('feature_branch')
    ws_path = get_ws_path(task_id)

    # todo clone template from git(by independent config)
    if GRADE == "base":
        success = True
    else:
        success = pullCode(ws_path, repo_path, base_branch, fature_branch)

    if success:
        return _("Create workspace successfully.")
    else:
        raise Exception(_("Failed to create workspace."))

@bp.route('/gitpush', methods=['POST'])
@json_response
def gitpush():
    _ = getI18n("controllers")
    args = request.json
    userPrompt = args['text']
    frontUuid = args['frontUuid']
    userName = session['username']
    
    pattern = r'(\S+:\S+:\S+)'
    matches = re.findall(pattern, userPrompt)
    parts = matches[0].split(':')
    session[userName]['memory']["repoPath"] = parts[0] + \
        ":"+parts[1]+":"+parts[2]

    pattern = r"```\n(.*?)\n```"
    match = re.search(pattern, userPrompt, re.DOTALL)
    code = ""
    if match:
        code = match.group(1)
    else:
        return

    pattern = r"commitMsg:(.*)"
    match = re.search(pattern, userPrompt, re.DOTALL)
    commitMsg = ""
    if match:
        commitMsg = match.group(1)
    print("match:"+match.group(1))

    plugin = {"name": 'push_code', "uuid": frontUuid}

    createBranch(session[userName]['memory']['appconfig']['sourceBranch'],
                            session[userName]['memory']['appconfig']['featureBranch'], parts[0])
    result, success = pushCode(
        parts[2], session[userName]['memory']['appconfig']['featureBranch'], parts[0], code, commitMsg)
    newPrompt = "基于 " + \
        session[userName]['memory']["repoPath"]+" 代码分支进行自动化集成测试"
    
    return 