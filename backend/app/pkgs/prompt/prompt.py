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
from config import GRADE

def clarifyRequirement(requirementID, userPrompt, globalContext, appArchitecture):
    if GRADE == "base":
        obj = RequirementBasic()
    else:
        obj = RequirementPro()
        
    return obj.clarifyRequirement(requirementID, userPrompt, globalContext, appArchitecture)

def clarifyAPI(requirementID, userPrompt, apiDoc):
    if GRADE == "base":
        obj = ApiBasic()
    else:
        obj = ApiPro()
        
    return obj.clarifyAPI(requirementID, userPrompt, apiDoc)

def splitTask(requirementID, newfeature, serviceName, appBasePrompt, projectInfo, projectLib, serviceStruct, appID):
    if GRADE == "base":
        obj = SubtaskBasic()
    else:
        if "java" in serviceName:
            obj = SubtaskJavaPro()
        if "vue" in serviceName:
            obj = SubtaskVuePro()
        else:
            obj = SubtaskPro()

    return obj.splitTask(requirementID, newfeature, serviceName, appBasePrompt, projectInfo, projectLib, serviceStruct, appID)

def aiReferenceRepair(requirementID, newCode, referenceCode, fileTask):
    if GRADE == "base":
        obj = CodeBasic()
    else:
        obj = CodePro()
        
    return obj.aiReferenceRepair(requirementID, newCode, referenceCode, fileTask)

def aiAnalyzeError(requirementID, message):
    if GRADE == "base":
        obj = CodeBasic()
    else:
        obj = CodePro()
        
    return obj.aiAnalyzeError(requirementID, message)

def aiFixError(requirementID, solution, code):
    if GRADE == "base":
        obj = CodeBasic()
    else:
        obj = CodePro()
        
    return obj.aiFixError(requirementID, solution, code)

def aiCheckCode(requirementID, fileTask, code):
    if GRADE == "base":
        obj = CodeBasic()
    else:
        obj = CodePro()
        
    return obj.aiCheckCode(requirementID, fileTask, code)

def aiMergeCode(requirementID, fileTask, appName, baseCode, newCode):
    if GRADE == "base":
        obj = CodeBasic()
    else:
        obj = CodePro()
        
    return obj.aiMergeCode(requirementID, fileTask, appName, baseCode, newCode)

def aiGenCode(requirementID, fileTask, newTask, newCode):
    if GRADE == "base":
        obj = CodeBasic()
    else:
        obj = CodePro()
        
    return obj.aiGenCode(requirementID, fileTask, newTask, newCode)