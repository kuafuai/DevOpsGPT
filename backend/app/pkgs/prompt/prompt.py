from app.pkgs.tools import storage
from app.pkgs.prompt.subtask_pro import SubtaskPro
from app.pkgs.prompt.requirement_basic import RequirementBasic
from app.pkgs.prompt.requirement_pro import RequirementPro
from app.pkgs.prompt.api_pro import ApiPro
from app.pkgs.prompt.api_basic import ApiBasic
from app.pkgs.prompt.subtask_basic import SubtaskBasic
from app.pkgs.prompt.subtask_java_pro import SubtaskJavaPro
from app.pkgs.prompt.subtask_python_pro import SubtaskPythonPro
from app.pkgs.prompt.subtask_vue_pro import SubtaskVuePro
from app.pkgs.prompt.code_basic import CodeBasic
from app.pkgs.prompt.code_pro import CodePro
from app.models.tenant_pro import Tenant
from config import GRADE

def pre_check_quota(func):
    def wrapper(*args, **kwargs):
        # 在方法调用前执行的代码
        if GRADE != "base":
            tenantID = storage.get("tenant_id")
            passed, msg = Tenant.check_quota(tenantID)
            if not passed:
                raise Exception(msg)
            print("pre_check_quota===========")
            print(passed)
            print(tenantID)

        # 调用原始方法
        result = func(*args, **kwargs)
        # 返回原始方法的结果
        return result
    return wrapper

@pre_check_quota
def clarifyRequirement(requirementID, userPrompt, globalContext, appArchitecture, req):
    if GRADE == "base":
        obj = RequirementBasic()
    else:
        obj = RequirementPro()
        
    return obj.clarifyRequirement(requirementID, userPrompt, globalContext, appArchitecture, req)

@pre_check_quota
def clarifyAPI(requirementID, userPrompt, apiDoc):
    if GRADE == "base":
        obj = ApiBasic()
    else:
        obj = ApiPro()
        
    return obj.clarifyAPI(requirementID, userPrompt, apiDoc)

@pre_check_quota
def splitTask(projectInfo, requirementID, newfeature, serviceName, appBasePrompt, projectIntro, projectLib, serviceStruct, appID, tenant_id):
    language = projectInfo["language"].lower()
    print("splitTask language:"+language)
    if GRADE == "base":
        obj = SubtaskBasic()
    else:
        if "java" in language:
            obj = SubtaskJavaPro()
        elif "python" in language:
            obj = SubtaskPythonPro()
        else:
            obj = SubtaskPro()

    return obj.splitTask(requirementID, newfeature, serviceName, appBasePrompt, projectIntro, projectLib, serviceStruct, appID, tenant_id)

@pre_check_quota
def splitTaskDo(req_info, service_info, tec_doc, tenant_id):
    if GRADE == "base":
        obj = SubtaskBasic()
    else:
        language = service_info["language"].lower()
        if "java" in language:
            obj = SubtaskJavaPro()
        elif "python" in language:
            obj = SubtaskPythonPro()
        else:
            obj = SubtaskPro()

    return obj.splitTaskDo(req_info, service_info, tec_doc, tenant_id)

@pre_check_quota
def aiReferenceRepair(requirementID, newCode, referenceCode, fileTask, filePath):
    if GRADE == "base":
        obj = CodeBasic()
    else:
        obj = CodePro()
        
    return obj.aiReferenceRepair(requirementID, newCode, referenceCode, fileTask, filePath)

@pre_check_quota
def aiAnalyzeError(requirementID, message, filePath):
    if GRADE == "base":
        obj = CodeBasic()
    else:
        obj = CodePro()
        
    return obj.aiAnalyzeError(requirementID, message, filePath)

@pre_check_quota
def aiFixError(requirementID, error_msg, solution, code, filePath, type):
    if GRADE == "base":
        obj = CodeBasic()
    else:
        obj = CodePro()
        
    return obj.aiFixError(requirementID, error_msg, solution, code, filePath, type)

@pre_check_quota
def aiCheckCode(requirementID, fileTask, code, filePath, service_name):
    if GRADE == "base":
        obj = CodeBasic()
    else:
        obj = CodePro()
        
    return obj.aiCheckCode(requirementID, fileTask, code, filePath, service_name)

@pre_check_quota
def aiMergeCode(requirementID, fileTask, baseCode, newCode, filePath):
    if GRADE == "base":
        obj = CodeBasic()
    else:
        obj = CodePro()
        
    return obj.aiMergeCode(requirementID, fileTask, baseCode, newCode, filePath)

@pre_check_quota
def aiGenCode(requirementID, fileTask, newTask, newCode, filePath):
    if GRADE == "base":
        obj = CodeBasic()
    else:
        obj = CodePro()
        
    return obj.aiGenCode(requirementID, fileTask, newTask, newCode, filePath)

def gen_write_code(requirement_id, service_name, file_path, development_detail, step_id):
    print("=============")
    print(requirement_id)
    print(service_name)
    print(file_path)
    print(development_detail)
    print(step_id)

    if GRADE == "base":
        obj = SubtaskBasic()
    else:
        if "java" in service_name:
            obj = SubtaskJavaPro()
        elif "python" in service_name:
            obj = SubtaskPythonPro()
        elif "vue" in service_name:
            obj = SubtaskVuePro()
        else:
            obj = SubtaskPro()

    jsonData = {"reasoning": development_detail, "code": ""}
    success = True
    
    re = obj.write_code(requirement_id, service_name, file_path, development_detail, step_id)
    jsonData["code"] = re[0]["content"]

    return jsonData, success
