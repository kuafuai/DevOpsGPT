from app.pkgs.prompt.subtask_interface import SubtaskInterface
from app.pkgs.prompt.subtask_pro import SubtaskPro

class SubtaskPythonPro(SubtaskInterface):
    def splitTask(self, requirementID, newfeature, serviceName, appBasePrompt, projectInfo, projectLib, serviceStruct,
                  appID):
        # The current version does not support this feature
        return SubtaskPro.splitTask(requirementID, newfeature, serviceName, appBasePrompt, projectInfo, projectLib,
                                    serviceStruct, appID)

    def write_code(self, requirement_id, service_name, file_path, development_detail, step_id):
        return SubtaskPro.write_code(requirement_id, service_name, file_path, development_detail, step_id)