from flask import request, session
from app.controllers.common import json_response
from flask import Blueprint
from app.pkgs.tools.i18b import getI18n
from app.pkgs.prompt.prompt import clarifyRequirement
from app.pkgs.knowledge.app_info import getAppArchitecture
from app.models.requirement import Requirement
from app.models.tenant_pro import Tenant
from app.models.tenant_bill_pro import TenantBill
from config import GRADE
from config import REQUIREMENT_STATUS_InProgress

bp = Blueprint('step_requirement', __name__, url_prefix='/step_requirement')

@bp.route('/clarify', methods=['POST'])
@json_response
def clarify():
    _ = getI18n("controllers")
    userPrompt = request.json.get('user_prompt')
    globalContext = request.json.get('global_context')
    userName = session["username"]
    requirementID = request.json.get('task_id')
    tenantID = session['tenant_id']

    req = Requirement.get_requirement_by_id(requirementID) 

    if not req or req["app_id"] < 1 :
        raise Exception(_("Please select the application you want to develop."))
    
    if len(globalContext) < 4 :
        Requirement.update_requirement(requirement_id=requirementID, requirement_name=userPrompt, status=REQUIREMENT_STATUS_InProgress)

        # 开始创建一个需求账单
        if GRADE != "base":
            TenantBill.record_requirement(tenantID, userName, requirementID, userPrompt)
    
    appArchitecture, _ = getAppArchitecture(req["app_id"])
    msg, success = clarifyRequirement(requirementID, userPrompt, globalContext, appArchitecture)

    if success:
        return {'message': msg, 'memory': session[userName]['memory'], "input_prompt": userPrompt}
    else:
        raise Exception(_("Failed to clarify requirement."))
