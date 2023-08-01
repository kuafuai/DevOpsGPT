from app.pkgs.prompt.subtask_interface import SubtaskInterface

class SubtaskJavaPro(SubtaskInterface):
    def splitTask(self, feature, serviceName, apiDocUrl):
        # The current version does not support this feature
        return "", False