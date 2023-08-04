from abc import ABC, abstractmethod

from config import GRADE

class CodeInterface(ABC):
    @abstractmethod
    def aiReferenceRepair(self, newCode, referenceCode, fileTask):
        pass

    @abstractmethod
    def aiAnalyzeError(self, message):
        pass

    @abstractmethod
    def aiFixError(self, solution, code):
        pass

    @abstractmethod
    def aiCheckCode(self, fileTask, code):
        pass

    @abstractmethod
    def aiMergeCode(self, task, baseCode, newCode):
        pass

    @abstractmethod
    def aiGenCode(self, fileTask, newTask, newCode):
        pass