from flask import request, session
from app.controllers.common import json_response
from app.pkgs.devops.local_tools import getFileContent
from app.pkgs.tools.i18b import getI18n
from app.pkgs.tools.file_tool import get_ws_path
from flask import Blueprint
from app.pkgs.prompt.prompt import splitTask
from app.pkgs.knowledge.app_info import getServiceSwagger
from app.pkgs.knowledge.app_info import getServiceBasePrompt, getServiceIntro, getServiceLib, getServiceStruct

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

    # todo Use llm to determine which interface documents to adjust
    appID = session[username]['memory']['task_info']['app_id']
    defaultApiDoc, success = getServiceSwagger(appID, 0)

    if len(defaultApiDoc) > 0:
        newfeature = requirementDoc+"""

You need to think on the basis of the following interface documentation：
```
"""+apiDoc.replace("```", "")+"""
```
"""
    else:
        newfeature = requirementDoc
        
    appBasePrompt, _ = getServiceBasePrompt(appID, serviceName)
    projectInfo, _ = getServiceIntro(appID, serviceName)
    projectLib, _ = getServiceLib(appID, serviceName)
    serviceStruct,_ = getServiceStruct(appID, serviceName)

    filesToEdit, success = splitTask(newfeature, serviceName, appBasePrompt, projectInfo, projectLib, serviceStruct, appID)

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