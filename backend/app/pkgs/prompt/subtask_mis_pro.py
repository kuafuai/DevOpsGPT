from app.pkgs.prompt.subtask_interface import SubtaskInterface

class SubtaskMisPro(SubtaskInterface):
    def splitTask(self, requirementID, newfeature, serviceName, appBasePrompt, projectInfo, projectLib, serviceStruct,
                  appID, tenant_id):

        return "", False

    def splitTaskDo(self, req_info, service_info, tec_doc, tenant_id):

        return "", False

    def write_code(self, requirement_id, service_name, file_path, development_detail, step_id):
        pass

