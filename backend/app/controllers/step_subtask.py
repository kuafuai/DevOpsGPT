from flask import request
from app.pkgs.tools import storage
from app.controllers.common import json_response
from app.pkgs.devops.local_tools import getFileContent
from app.pkgs.tools.i18b import getI18n
from flask import Blueprint
from app.pkgs.prompt.prompt import splitTask, splitTaskDo
from app.pkgs.knowledge.app_info import getServiceBasePrompt, getServiceInfo, getServiceIntro, getServiceLib, getServiceStruct
from app.models.requirement import Requirement
from app.models.application_service import ApplicationService
from app.pkgs.tools.file_tool import get_base_path, get_ws_path

bp = Blueprint('step_subtask', __name__, url_prefix='/step_subtask')

@bp.route('/analysis', methods=['POST'])
@json_response
def analysis():
    _ = getI18n("controllers")
    data = request.json
    serviceName = data['service_name']
    prompt = data['prompt']
    doc_type = data['doc_type']
    username = storage.get("username")
    requirementID = request.json.get('task_id')
    tenantID = storage.get("tenant_id")

    req = Requirement.get_requirement_by_id(requirementID, tenantID) 

    if doc_type == "api":
        requirementDoc = req["original_requirement"]
        newfeature = requirementDoc+"""

You need to think on the basis of the following interface documentation：
```
"""+prompt.replace("```", "")+"""
```
"""
    else:
        requirementDoc = prompt
        Requirement.update_requirement(requirement_id=requirementID, tenant_id=tenantID, original_requirement=prompt)
        newfeature = requirementDoc
        
    appBasePrompt, _ = getServiceBasePrompt(req["app_id"], serviceName)
    projectIntro, _ = getServiceIntro(req["app_id"], serviceName, tenantID)
    projectLib, _ = getServiceLib(req["app_id"], serviceName)
    serviceStruct, _ = getServiceStruct(req["app_id"], serviceName)
    projectInfo, _ = getServiceInfo(req["app_id"], serviceName, tenantID)

    subtask, success = splitTask(projectInfo, requirementID, newfeature, serviceName, appBasePrompt, projectIntro, projectLib, serviceStruct, req["app_id"], tenantID)

    if success and subtask:
        return {'message': subtask, 'service_name': serviceName}
    else:
        raise Exception(_("Failed to split task."))
    
@bp.route('/task_split', methods=['POST'])
@json_response
def task_split():
    _ = getI18n("controllers")
    data = request.json
    service_name = data['service_name']
    tec_doc = data['prompt']
    task_id = request.json.get('task_id')
    tenant_id = storage.get("tenant_id")

    req_info = Requirement.get_requirement_by_id(task_id, tenant_id) 
    service_info = ApplicationService.get_service_by_name(req_info["app_id"], service_name)

    filesToEdit, success = splitTaskDo(req_info, service_info, tec_doc, tenant_id)

    git_path = service_info["git_path"]
    bath_path = get_base_path(task_id, git_path)
    if success and filesToEdit:
        for index, file in enumerate(filesToEdit):
            file_path = file["file-path"] if 'file-path' in file else file["file_path"]
            isSuccess, oldCode = getFileContent(file_path, bath_path)
            filesToEdit[index]["old-code"] = oldCode
            if not isSuccess:
                filesToEdit[index]["old-code"] = ''

            reference_file = file["reference-file"] if 'reference-file' in file else ''
            isSuccess, referenceCode = getFileContent(reference_file, bath_path)
            filesToEdit[index]["reference-code"] = referenceCode
            if not isSuccess:
                filesToEdit[index]["reference-code"] = ''
    
        plugin = {"name": 'task_list', "info": {"files":filesToEdit, "service_name": service_name}}

        return {'plugin': plugin}
    else:
        raise Exception(_("Failed to split task."))
