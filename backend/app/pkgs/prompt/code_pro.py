from app.pkgs.prompt.code_interface import CodeInterface

class CodePro(CodeInterface):
    def aiReferenceRepair(self, newCode, referenceCode, fileTask):
        # The current version does not support this feature
        return [], False

    def aiAnalyzeError(self, message):
        # The current version does not support this feature
        return [], False

    def aiFixError(self, solution, code):
        # The current version does not support this feature
        return [], False

    def aiCheckCode(self, fileTask, code):
        # The current version does not support this feature
        return [], False

    def aiMergeCode(self, task, baseCode, newCode):
        # The current version does not support this feature
        return [], False

    def aiGenCode(self, fileTask, newTask, newCode):
        # The current version does not support this feature
        return [], False
