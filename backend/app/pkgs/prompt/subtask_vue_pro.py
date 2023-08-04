from app.pkgs.prompt.subtask_interface import SubtaskInterface

class SubtaskVuePro(SubtaskInterface):
    def splitTask(self, newfeature, serviceName, appBasePrompt, projectInfo, projectLib, serviceStruct, appID):
        # The current version does not support this feature
        return "", False
