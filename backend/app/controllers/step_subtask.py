from flask import request
from app.pkgs.tools import storage
from app.controllers.common import json_response
from app.pkgs.devops.local_tools import getFileContent
from app.pkgs.tools.i18b import getI18n
from flask import Blueprint
from app.pkgs.prompt.prompt import splitTask
from app.pkgs.knowledge.app_info import getServiceBasePrompt, getServiceIntro, getServiceLib, getServiceStruct
from app.models.requirement import Requirement

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
    req = Requirement.get_requirement_by_id(requirementID) 

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
        Requirement.update_requirement(requirement_id=requirementID, original_requirement=prompt)
        newfeature = requirementDoc
        
    appBasePrompt, _ = getServiceBasePrompt(req["app_id"], serviceName)
    projectInfo, _ = getServiceIntro(req["app_id"], serviceName)
    projectLib, _ = getServiceLib(req["app_id"], serviceName)
    serviceStruct, _ = getServiceStruct(req["app_id"], serviceName)

    filesToEdit, success = splitTask(requirementID, newfeature, serviceName, appBasePrompt, projectInfo, projectLib, serviceStruct, req["app_id"])

    if success and filesToEdit:
        for index, file in enumerate(filesToEdit):
            file_path = file["file-path"] if 'file-path' in file else file["file_path"]
            isSuccess, oldCode = getFileContent(file_path, serviceName)
            filesToEdit[index]["old-code"] = oldCode
            if not isSuccess:
                filesToEdit[index]["old-code"] = ''

            reference_file = file["reference-file"] if 'reference-file' in file else ''
            isSuccess, referenceCode = getFileContent(reference_file, serviceName)
            filesToEdit[index]["reference-code"] = referenceCode
            if not isSuccess:
                filesToEdit[index]["reference-code"] = ''
    
        plugin = {"name": 'task_list', "info": {"files":filesToEdit, "service_name": serviceName}}

        return {'plugin': plugin}
    else:
        raise Exception(_("Failed to split task."))
