from abc import ABC, abstractmethod

from config import GRADE

class CodeInterface(ABC):
    @abstractmethod
    def aiReferenceRepair(self, requirementID, newCode, referenceCode, fileTask, filePath):
        pass

    @abstractmethod
    def aiAnalyzeError(self, requirementID, message, filePath):
        pass

    @abstractmethod
    def aiFixError(self, requirementID, solution, code, filePath, type):
        pass

    @abstractmethod
    def aiCheckCode(self, requirementID, fileTask, code, filePath):
        pass

    @abstractmethod
    def aiMergeCode(self, requirementID, task, baseCode, newCode, filePath):
        pass

    @abstractmethod
    def aiGenCode(self, requirementID, fileTask, newTask, newCode, filePath):
        pass