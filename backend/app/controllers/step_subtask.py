import time
from flask import request, session
from app.controllers.common import json_response
from app.pkgs.prompt.subtask import splitTask
from app.pkgs.prompt.subtask_java_pro import splitTaskJavaPro
from app.pkgs.prompt.subtask_vue_pro import splitTaskVuePro
from app.pkgs.devops.devops import get_file_content
from app.pkgs.tools.i18b import getI18n
from app.pkgs.knowledge.app_info import getSwagger
from config import GRADE
from app.pkgs.tools.file_tool import get_ws_path
from flask import Blueprint

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
        
    if GRADE == "base":
        filesToEdit, success = splitTask(newfeature, serviceName, apiDocUrl)
    else:
        if "java" in serviceName:
            filesToEdit, success = splitTaskJavaPro(newfeature, serviceName, wsPath)
        if "vue" in serviceName:
            filesToEdit, success = splitTaskVuePro(newfeature, serviceName)
        else:
            filesToEdit, success = splitTask(newfeature, serviceName)

    if success:
        for serviceIdx, service in enumerate(filesToEdit):
            for index, file in enumerate(service["files"]):
                isSuccess, oldCode = get_file_content(file["file-path"], sourceBranch, filesToEdit[serviceIdx]["service-name"])
                filesToEdit[serviceIdx]["files"][index]["old-code"] = oldCode
                if not isSuccess:
                    filesToEdit[serviceIdx]["files"][index]["old-code"] = ''

                isSuccess, referenceCode = get_file_content(file["reference-file"], sourceBranch, filesToEdit[serviceIdx]["service-name"])
                filesToEdit[serviceIdx]["files"][index]["reference-code"] = referenceCode
                if not isSuccess:
                    filesToEdit[serviceIdx]["files"][index]["reference-code"] = ''
    
        plugin = {"name": 'task_list', "info": filesToEdit}
        session[username]['memory']['tasks'] = filesToEdit # 这里不更新session，只给前端用

        return {'plugin': plugin, 'memory': session[username]['memory']}
    else:
        raise Exception(_("Failed to split task."))