from flask import request, session
from app.controllers.common import json_response
from app.pkgs.devops.local_tools import getFileContent
from app.pkgs.tools.i18b import getI18n
from app.pkgs.knowledge.app_info import getSwagger
from app.pkgs.tools.file_tool import get_ws_path
from flask import Blueprint
from app.pkgs.prompt.prompt import splitTask

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
    appName = session[username]['memory']['appconfig']['appName']
    sourceBranch = session[username]['memory']['appconfig']['sourceBranch']
    apiDocUrl = session[username]['memory']['appconfig']['apiDocUrl']
    wsPath = get_ws_path(session[username]['memory']['appconfig']['taskID'])

    defaultSwaggerDoc, success = getSwagger(apiDocUrl)
    if len(defaultSwaggerDoc) > 0:
        newfeature = requirementDoc+"""

接口文档：
```
"""+apiDoc+"""
```
"""
    else:
        newfeature = requirementDoc
        
    filesToEdit, success = splitTask(newfeature, serviceName, apiDocUrl)

    if success:
        for serviceIdx, service in enumerate(filesToEdit):
            for index, file in enumerate(service["files"]):
                isSuccess, oldCode = getFileContent(file["file-path"], sourceBranch, filesToEdit[serviceIdx]["service-name"])
                filesToEdit[serviceIdx]["files"][index]["old-code"] = oldCode
                if not isSuccess:
                    filesToEdit[serviceIdx]["files"][index]["old-code"] = ''

                isSuccess, referenceCode = getFileContent(file["reference-file"], sourceBranch, filesToEdit[serviceIdx]["service-name"])
                filesToEdit[serviceIdx]["files"][index]["reference-code"] = referenceCode
                if not isSuccess:
                    filesToEdit[serviceIdx]["files"][index]["reference-code"] = ''
    
        plugin = {"name": 'task_list', "info": filesToEdit}
        session[username]['memory']['tasks'] = filesToEdit # 这里不更新session，只给前端用

        return {'plugin': plugin, 'memory': session[username]['memory']}
    else:
        raise Exception(_("Failed to split task."))