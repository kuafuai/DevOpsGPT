from flask import request
from app.controllers.common import json_response
from flask import Blueprint

from app.pkgs.knowledge.app_info import repo_analyzer
from app.pkgs.tools.i18b import getI18n
from app.models.async_task import AsyncTask

bp = Blueprint('plugine', __name__, url_prefix='/plugine')


@bp.route('/repo_analyzer', methods=['GET'])
@json_response
def repo_analyzer_plugine():
    _ = getI18n("controllers")

    type = request.args.get("type")
    repo = request.args.get("repo")
    if type is None or repo is None:
        raise Exception("param error")
    if len(type) == 0 or len(repo) == 0:
        raise Exception("param error")

    data = {"type": type, "repo": repo}

    task = AsyncTask.create_task(AsyncTask.Type_Analyzer_Code, "分析代码仓库", str(data))
    if task:
        return {"task_no": task.token}
    else:
        raise Exception("服务器异常")


@bp.route('/repo_analyzer_check', methods=['GET'])
@json_response
def repo_analyzer_check():
    task_no = request.args.get("task_no")
    if task_no is None or len(task_no) == 0:
        raise Exception("param error")

    task = AsyncTask.get_task_by_token(task_no)
    if task:
        return {"task_no": task.token, "status": task.task_status, "message": task.task_status_message}
    else:
        raise Exception("服务器异常")
