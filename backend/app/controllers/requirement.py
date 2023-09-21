from flask import Blueprint, request
from app.controllers.common import json_response
from app.pkgs.tools.i18b import getI18n
from app.models.requirement import Requirement
from app.models.requirement_memory_pro import RequirementMemory
from app.models.tenant_pro import Tenant
from app.models.tenant_bill_pro import TenantBill
from app.pkgs.tools import storage
from config import REQUIREMENT_STATUS_NotStarted, GRADE

bp = Blueprint('requirement', __name__, url_prefix='/requirement')


@bp.route('/clear_up', methods=['GET'])
@json_response
def clear_up():
    if GRADE != "base":
        tenant = Tenant.get_tenant_baseinfo_by_id(storage.get("tenant_id"))
        if tenant:
            tenant_name = tenant["name"]
            billing_type_name = tenant["billing_type_name"]
            code_power = TenantBill.get_total_codepower(storage.get("tenant_id"))
    else:
        tenant_name = "DevOpsGPT"
        code_power = '0'
        billing_type_name = "FREE"

    return {"username": storage.get("username"), "billing_type_name": billing_type_name, "tenant_name": tenant_name, "tenant_id": storage.get("tenant_id"), "code_power": code_power}


@bp.route('/setup_app', methods=['POST'])
@json_response
def setup_app():
    _ = getI18n("controllers")
    data = request.json
    appID = data['app_id']
    sourceBranch = data['source_branch']
    featureBranch = data['feature_branch']
    username = storage.get("username")
    tenantID = storage.get("tenant_id")

    if GRADE != "base":
        passed, msg = Tenant.check_quota(tenantID)
        if not passed:
            raise Exception(msg)

    requirement = Requirement.create_requirement(
        tenantID, "New requirement", "New", appID, username, sourceBranch, featureBranch,  REQUIREMENT_STATUS_NotStarted, 0, 0)

    if requirement.requirement_id:
        return Requirement.get_requirement_by_id(requirement.requirement_id, tenantID)
    else:
        raise Exception(_("Failed to set up app."))


@bp.route('/get', methods=['GET'])
@json_response
def get_all():
    _ = getI18n("controllers")
    tenantID = storage.get("tenant_id")

    requirements = Requirement.get_all_requirements(tenantID, 1, 100)

    return {'requirements': requirements["requirements"]}


@bp.route('/get_one', methods=['GET'])
@json_response
def get_one():
    _ = getI18n("controllers")
    requirementID = request.args.get('requirement_id')
    tenantID = storage.get("tenant_id")

    requirement = Requirement.get_requirement_by_id(requirementID, tenantID)
    if not requirement:
        raise Exception(_("The task does not exist.")) 

    memory = {
        "task_info": {
            "app_id": requirement["app_id"],
            "task_id": requirement["requirement_id"],
            "source_branch": requirement["default_source_branch"],
            "feature_branch": requirement["default_target_branch"]
        }
    }
    requirement["old_memory"] = memory

    if GRADE != "base":
        requirement["memory"] = RequirementMemory.get_all_requirement_memories(
            requirementID, 1)

    return requirement


@bp.route('/update', methods=['POST'])
@json_response
def update():
    _ = getI18n("controllers")
    data = request.json
    requirement_id = data['requirement_id']
    update_data = data['data']
    tenantID = storage.get("tenant_id")

    requirement = Requirement.update_requirement(requirement_id, tenantID, **update_data)

    if requirement.requirement_id:
        return Requirement.get_requirement_by_id(requirement.requirement_id, tenantID)
    else:
        raise Exception(_("Failed to set up app."))
