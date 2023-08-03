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
    wsPath = get_ws_path(session[username]['memory']['task_info']['task_id'])

    # todo Use llm to determine which interface documents to adjust
    appID = session[username]['memory']['task_info']['app_id']
    defaultApiDoc, success = getServiceSwagger(appID, 1)

    if len(defaultApiDoc) > 0:
        newfeature = requirementDoc+"""

接口文档：
```
"""+apiDoc+"""
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
        for serviceNamex, service in enumerate(filesToEdit):
            for index, file in enumerate(service["files"]):
                isSuccess, oldCode = getFileContent(file["file-path"], sourceBranch, filesToEdit[serviceNamex]["service-name"])
                filesToEdit[serviceNamex]["files"][index]["old-code"] = oldCode
                if not isSuccess:
                    filesToEdit[serviceNamex]["files"][index]["old-code"] = ''

                isSuccess, referenceCode = getFileContent(file["reference-file"], sourceBranch, filesToEdit[serviceNamex]["service-name"])
                filesToEdit[serviceNamex]["files"][index]["reference-code"] = referenceCode
                if not isSuccess:
                    filesToEdit[serviceNamex]["files"][index]["reference-code"] = ''
    
        plugin = {"name": 'task_list', "info": filesToEdit}
        session[username]['memory']['tasks'] = filesToEdit # 这里不更新session，只给前端用

        return {'plugin': plugin, 'memory': session[username]['memory']}
    else:
        raise Exception(_("Failed to split task."))