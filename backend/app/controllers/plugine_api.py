from flask import request
from app.controllers.common import json_response
from flask import Blueprint

from app.pkgs.knowledge.app_info import repo_analyzer
from app.pkgs.tools.i18b import getI18n

bp = Blueprint('plugine', __name__, url_prefix='/plugine')


@bp.route('/repo_analyzer', methods=['GET'])
@json_response
def repo_analyzer_plugine():
    _ = getI18n("controllers")

    type = request.args.get("type")
    repo = request.args.get("repo")
    print(type, repo)
    info, success = repo_analyzer(type, repo)
    if not success:
        raise Exception(
            _("Failed to analysis applications.") + "（AI 自动导入已有代码库新建应用功能，目前只支持Java和python语言，其它语言可通过<a href='/app.html?action=create_new_tpl'>模板创建</a>。 Currently, AI import existing code project only Java and python languages are supported. For other languages, use <a href='/app.html? action=create_new_tpl'> Template creation </a>）")

    return info
