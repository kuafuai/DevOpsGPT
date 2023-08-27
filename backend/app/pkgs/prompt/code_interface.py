from abc import ABC, abstractmethod

from config import GRADE

class CodeInterface(ABC):
    @abstractmethod
    def aiReferenceRepair(self, requirementID, newCode, referenceCode, fileTask):
        pass

    @abstractmethod
    def aiAnalyzeError(self, requirementID, message):
        pass

    @abstractmethod
    def aiFixError(self, requirementID, solution, code):
        pass

    @abstractmethod
    def aiCheckCode(self, requirementID, fileTask, code):
        pass

    @abstractmethod
    def aiMergeCode(self, requirementID, task, baseCode, newCode):
        pass

    @abstractmethod
    def aiGenCode(self, requirementID, fileTask, newTask, newCode):
        pass