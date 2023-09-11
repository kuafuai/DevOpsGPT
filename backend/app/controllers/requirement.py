from flask import Blueprint, request, session, json
from app.controllers.common import json_response
from app.models.task import getEmptyTaskInfo
from app.pkgs.tools.i18b import getI18n
from app.models.requirement import Requirement
from app.models.requirement_memory_pro import RequirementMemory
from app.models.tenant_pro import Tenant
from app.models.tenant_bill_pro import TenantBill
from config import REQUIREMENT_STATUS_NotStarted, GRADE

bp = Blueprint('requirement', __name__, url_prefix='/requirement')

@bp.route('/clear_up', methods=['GET'])
@json_response
def clear_up(): 
    try:
        session.pop(session["username"])
    except Exception as e:
        print("clear_up failed:"+str(e))
    
    session[session["username"]] = getEmptyTaskInfo()
    tenant_name = "-"
    code_power = '0'
    if GRADE != "base":
        tenant = Tenant.get_tenant_baseinfo_by_id(session["tenant_id"])
        if tenant:
            tenant_name = tenant["name"]
            code_power = TenantBill.get_total_codepower(session["tenant_id"])

    return {"username": session["username"], "tenant_name": tenant_name, "tenant_id": session["tenant_id"], "info": session[session["username"]], "code_power": code_power} 


@bp.route('/setup_app', methods=['POST'])
@json_response
def setup_app():
    _ = getI18n("controllers")
    data = request.json
    appID = data['app_id']
    sourceBranch = data['source_branch']
    featureBranch = data['feature_branch']
    username = session['username']
    tenantID = session['tenant_id']

    if GRADE != "base":
        passed, msg = Tenant.check_quota(tenantID)
        if not passed:
            raise Exception(msg)

    requirement = Requirement.create_requirement(tenantID, "New requirement", "New", appID, username, sourceBranch, featureBranch,  REQUIREMENT_STATUS_NotStarted, 0, 0)

    session[username]['memory']['task_info'] = {
        "app_id": appID,
        "task_id": requirement.requirement_id,
        "source_branch": sourceBranch,
        "feature_branch": featureBranch
    }
    session.update()

    if requirement.requirement_id:
        return Requirement.get_requirement_by_id(requirement.requirement_id)
    else:
        raise Exception(_("Failed to set up app."))

@bp.route('/get', methods=['GET'])
@json_response
def get_all():
    _ = getI18n("controllers")
    tenantID = session['tenant_id']

    requirements = Requirement.get_all_requirements(tenantID)

    return {'requirements': requirements}
    
@bp.route('/get_one', methods=['GET'])
@json_response
def get_one():
    _ = getI18n("controllers")
    requirementID = request.args.get('requirement_id')

    requirement = Requirement.get_requirement_by_id(requirementID)

    memory = {
        "task_info" : {
            "app_id": requirement["app_id"],
            "task_id": requirement["requirement_id"],
            "source_branch": requirement["default_source_branch"],
            "feature_branch": requirement["default_target_branch"]
        }
    }
    requirement["old_memory"] = memory

    if GRADE != "base":
        requirement["memory"] = RequirementMemory.get_all_requirement_memories(requirementID, 1)

    return requirement

@bp.route('/update', methods=['POST'])
@json_response
def update():
    _ = getI18n("controllers")
    data = request.json
    requirement_id = data['requirement_id']
    update_data = data['data']

    requirement = Requirement.update_requirement(requirement_id, **update_data)

    if requirement.requirement_id:
        return Requirement.get_requirement_by_id(requirement.requirement_id)
    else:
        raise Exception(_("Failed to set up app."))