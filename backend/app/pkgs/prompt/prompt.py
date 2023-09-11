from flask import session
from app.pkgs.prompt.subtask_pro import SubtaskPro
from app.pkgs.prompt.requirement_basic import RequirementBasic
from app.pkgs.prompt.requirement_pro import RequirementPro
from app.pkgs.prompt.api_pro import ApiPro
from app.pkgs.prompt.api_basic import ApiBasic
from app.pkgs.prompt.subtask_basic import SubtaskBasic
from app.pkgs.prompt.subtask_java_pro import SubtaskJavaPro
from app.pkgs.prompt.subtask_vue_pro import SubtaskVuePro
from app.pkgs.prompt.code_basic import CodeBasic
from app.pkgs.prompt.code_pro import CodePro
from app.models.tenant_pro import Tenant
from config import GRADE

def pre_check_quota(func):
    def wrapper(*args, **kwargs):
        # 在方法调用前执行的代码
        if GRADE != "base":
            tenantID = session['tenant_id']
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
def clarifyRequirement(requirementID, userPrompt, globalContext, appArchitecture):
    if GRADE == "base":
        obj = RequirementBasic()
    else:
        obj = RequirementPro()
        
    return obj.clarifyRequirement(requirementID, userPrompt, globalContext, appArchitecture)

@pre_check_quota
def clarifyAPI(requirementID, userPrompt, apiDoc):
    if GRADE == "base":
        obj = ApiBasic()
    else:
        obj = ApiPro()
        
    return obj.clarifyAPI(requirementID, userPrompt, apiDoc)

@pre_check_quota
def splitTask(requirementID, newfeature, serviceName, appBasePrompt, projectInfo, projectLib, serviceStruct, appID):
    if GRADE == "base":
        obj = SubtaskBasic()
    else:
        if "java" in serviceName:
            obj = SubtaskJavaPro()
        elif "vue" in serviceName:
            obj = SubtaskVuePro()
        else:
            obj = SubtaskPro()

    return obj.splitTask(requirementID, newfeature, serviceName, appBasePrompt, projectInfo, projectLib, serviceStruct, appID)

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
def aiFixError(requirementID, solution, code, filePath, type):
    if GRADE == "base":
        obj = CodeBasic()
    else:
        obj = CodePro()
        
    return obj.aiFixError(requirementID, solution, code, filePath, type)

@pre_check_quota
def aiCheckCode(requirementID, fileTask, code, filePath):
    if GRADE == "base":
        obj = CodeBasic()
    else:
        obj = CodePro()
        
    return obj.aiCheckCode(requirementID, fileTask, code, filePath)

@pre_check_quota
def aiMergeCode(requirementID, fileTask, appName, baseCode, newCode, filePath):
    if GRADE == "base":
        obj = CodeBasic()
    else:
        obj = CodePro()
        
    return obj.aiMergeCode(requirementID, fileTask, appName, baseCode, newCode, filePath)

@pre_check_quota
def aiGenCode(requirementID, fileTask, newTask, newCode, filePath):
    if GRADE == "base":
        obj = CodeBasic()
    else:
        obj = CodePro()
        
    return obj.aiGenCode(requirementID, fileTask, newTask, newCode, filePath)

def gen_write_code(requirement_id, service_name, file_path, development_detail, step_id):
    if GRADE == "base":
        obj = SubtaskBasic()
    else:
        if "java" in service_name:
            obj = SubtaskJavaPro()
        elif "vue" in service_name:
            obj = SubtaskVuePro()
        else:
            obj = SubtaskPro()

    return obj.write_code(requirement_id, service_name, file_path, development_detail, step_id)
