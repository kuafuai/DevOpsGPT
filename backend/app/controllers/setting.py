from flask import request, session
from app.controllers.common import json_response
from flask import Blueprint
from app.pkgs.tools.i18b import getI18n
from app.models.setting import getGitConfigList, getCIConfigList, getCDConfigList, getLLMConfigList

bp = Blueprint('setting', __name__, url_prefix='/setting')

@bp.route('/get_git_config_list', methods=['GET'])
@json_response
def get_git_config_list():
    _ = getI18n("controllers")
    tenantID = session['tenant_id']

    gitList, success = getGitConfigList(tenantID, 0)
    if not success:
        raise Exception(_("Failed to get git config list.")) 

    return gitList

@bp.route('/get_ci_config_list', methods=['GET'])
@json_response
def get_ci_config_list():
    _ = getI18n("controllers")
    tenantID = session['tenant_id']

    gitList, success = getCIConfigList(tenantID, 0)
    if not success:
        raise Exception(_("Failed to get git config list.")) 

    return gitList

@bp.route('/get_cd_config_list', methods=['GET'])
@json_response
def get_cd_config_list():
    _ = getI18n("controllers")
    tenantID = session['tenant_id']

    gitList, success = getCDConfigList(tenantID, 0)
    if not success:
        raise Exception(_("Failed to get git config list.")) 

    return gitList

@bp.route('/get_llm_config_list', methods=['GET'])
@json_response
def get_llm_config_list():
    _ = getI18n("controllers")
    tenantID = session['tenant_id']

    gitList, success = getLLMConfigList(tenantID, 0)
    if not success:
        raise Exception(_("Failed to get git config list.")) 

    return gitList