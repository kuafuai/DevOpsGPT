from flask import request
from app.pkgs.tools import storage
from app.controllers.common import json_response
from flask import Blueprint
from app.pkgs.tools.i18b import getI18n
from app.models.setting import getGitConfigList, getCIConfigList, getCDConfigList, getLLMConfigList
from app.models.tenant_git_config_pro import TenantGitConfig
from app.models.tenant_cd_config_pro import TenantCDConfig
from app.models.tenant_ci_config_pro import TenantCIConfig

bp = Blueprint('setting', __name__, url_prefix='/setting')

@bp.route('/get_git_config_list', methods=['GET'])
@json_response
def get_git_config_list():
    _ = getI18n("controllers")
    tenantID = request.args.get('tenant_id')

    gitList, success = getGitConfigList(tenantID, 0)
    if not success:
        raise Exception(_("Failed to get git config list."))

    return gitList

@bp.route('/get_ci_config_list', methods=['GET'])
@json_response
def get_ci_config_list():
    _ = getI18n("controllers")
    tenantID = request.args.get('tenant_id')

    gitList, success = getCIConfigList(tenantID, 0)
    if not success:
        raise Exception(_("Failed to get git config list."))

    return gitList

@bp.route('/get_cd_config_list', methods=['GET'])
@json_response
def get_cd_config_list():
    _ = getI18n("controllers")
    tenantID = request.args.get('tenant_id')

    gitList, success = getCDConfigList(tenantID, 0)
    if not success:
        raise Exception(_("Failed to get git config list."))

    return gitList

@bp.route('/get_llm_config_list', methods=['GET'])
@json_response
def get_llm_config_list():
    _ = getI18n("controllers")
    raise Exception(_("Failed to get git config list."))
    tenantID = request.args.get('tenant_id')

    gitList, success = getLLMConfigList(tenantID, 0)
    if not success:
        raise Exception(_("Failed to get git config list."))

    return gitList

@bp.route('/edit_git', methods=['POST'])
@json_response
def edit_git():
    _ = getI18n("controllers")
    git_email = request.json.get('git_email')
    git_provider = request.json.get('git_provider')
    git_token = request.json.get('git_token')
    git_url = request.json.get('git_url')
    git_username = request.json.get('git_username')
    git_config_id = request.json.get('git_config_id')
    name = request.json.get('git_name')
    creater = storage.get("username")
    tenant_id = request.json.get('tenant_id')

    try:
        if git_config_id:
            generate_kwargs = dict(
                name=name,
                git_email=git_email,
                git_provider=git_provider,
                git_url=git_url,
                git_username=git_username
            )
            if git_token.find("*") == -1:
                generate_kwargs.update(dict(git_token=git_token))
            TenantGitConfig.update_config(git_config_id, tenant_id, **generate_kwargs)
            id = git_config_id
        else:
            data = TenantGitConfig.create_config(tenant_id, creater, name, git_url, git_token, git_provider, git_username, git_email)
            id = data.git_config_id

        return {'success': id}
    except Exception as e:
        raise Exception(_("Failed to edit setting."))

@bp.route('/edit_ci', methods=['POST'])
@json_response
def edit_ci():
    _ = getI18n("controllers")
    ci_api_url = request.json.get('ci_api_url')
    ci_token = request.json.get('ci_token')
    ci_provider = request.json.get('ci_provider')
    ci_config_id = request.json.get('ci_config_id')
    name = request.json.get('ci_name')
    creater = storage.get("username")
    tenant_id = request.json.get('tenant_id')

    try:
        if ci_config_id:
            generate_kwargs = dict(
                name=name,
                ci_api_url=ci_api_url,
                ci_provider=ci_provider
            )
            if ci_token.find("*") == -1:
                generate_kwargs.update(dict(ci_token=ci_token))
            TenantCIConfig.update_config(ci_config_id, tenant_id, **generate_kwargs)
            id = ci_config_id
        else:
            data = TenantCIConfig.create_config(tenant_id, creater, name, ci_api_url, ci_token, ci_provider)
            id = data.ci_config_id

        return {'success': id}
    except Exception as e:
        raise Exception(_("Failed to edit setting."))

@bp.route('/edit_cd', methods=['POST'])
@json_response
def edit_cd():
    _ = getI18n("controllers")
    cd_config_id = request.json.get('cd_config_id')
    access_key = request.json.get('ACCESS_KEY')
    secret_key = request.json.get('SECRET_KEY')
    cd_provider = request.json.get('cd_provider')
    name = request.json.get('cd_name')
    creater = storage.get("username")
    tenant_id = request.json.get('tenant_id')

    try:
        if cd_config_id:
            generate_kwargs = dict(
                name=name, cd_provider=cd_provider
            )
            if access_key.find("*") == -1:
                generate_kwargs.update(dict(access_key=access_key))
            if secret_key.find("*") == -1:
                generate_kwargs.update(dict(secret_key=secret_key))

            TenantCDConfig.update_config(cd_config_id, tenant_id, **generate_kwargs)
            id = cd_config_id
        else:
            data = TenantCDConfig.create_config(tenant_id, creater, name, access_key, secret_key, cd_provider)
            id = data.cd_config_id

        return {'success': id}
    except Exception as e:
        raise Exception(_("Failed to edit setting."))