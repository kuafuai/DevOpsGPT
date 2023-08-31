from flask import request, session
from app.controllers.common import json_response
from app.pkgs.devops.local_tools import getFileContent
from app.pkgs.tools.i18b import getI18n
from flask import Blueprint
from app.pkgs.prompt.prompt import splitTask
from app.pkgs.knowledge.app_info import getServiceSwagger
from app.pkgs.knowledge.app_info import getServiceBasePrompt, getServiceIntro, getServiceLib, getServiceStruct
from app.models.requirement import Requirement

bp = Blueprint('step_subtask', __name__, url_prefix='/step_subtask')

@bp.route('/analysis', methods=['POST'])
@json_response
def analysis():
    _ = getI18n("controllers")
    data = request.json
    serviceName = data['service_name']
    apiDoc = data['api_doc']
    username = session['username']
    requirementDoc = session[username]['memory']['originalPrompt']
    sourceBranch = session[username]['memory']['task_info']['source_branch']
    requirementID = request.json.get('task_id')

    # todo Use llm to determine which interface documents to adjust
    req = Requirement.get_requirement_by_id(requirementID) 
    defaultApiDoc, success = getServiceSwagger(req["app_id"], 0)

    if len(defaultApiDoc) > 0:
        newfeature = requirementDoc+"""

You need to think on the basis of the following interface documentation：
```
"""+apiDoc.replace("```", "")+"""
```
"""
    else:
        newfeature = requirementDoc
        
    appBasePrompt, _ = getServiceBasePrompt(req["app_id"], serviceName)
    projectInfo, _ = getServiceIntro(req["app_id"], serviceName)
    projectLib, _ = getServiceLib(req["app_id"], serviceName)
    serviceStruct, _ = getServiceStruct(req["app_id"], serviceName)

    filesToEdit, success = splitTask(requirementID, newfeature, serviceName, appBasePrompt, projectInfo, projectLib, serviceStruct, req["app_id"])

    if success:
        for index, file in enumerate(filesToEdit):
            isSuccess, oldCode = getFileContent(file["file-path"], sourceBranch, serviceName)
            filesToEdit[index]["old-code"] = oldCode
            if not isSuccess:
                filesToEdit[index]["old-code"] = ''

            isSuccess, referenceCode = getFileContent(file["reference-file"], sourceBranch, serviceName)
            filesToEdit[index]["reference-code"] = referenceCode
            if not isSuccess:
                filesToEdit[index]["reference-code"] = ''
    
        plugin = {"name": 'task_list', "info": {"files":filesToEdit, "service_name": serviceName}}
        session[username]['memory']['tasks'] = filesToEdit # There is no session update here, just for the frontend

        return {'plugin': plugin, 'memory': session[username]['memory']}
    else:
        raise Exception(_("Failed to split task."))