from abc import ABC, abstractmethod

from config import GRADE

class LocalToolsInterface(ABC):
    @abstractmethod
    def compileCheck(requirementID, ws_path,repo_path):
        pass

    @abstractmethod
    def lintCheck(requirementID, ws_path, repo_path, file_path):
        pass

    @abstractmethod
    def unitTest(requirementID, ws_path, repo_path, file_path):
        pass

    @abstractmethod
    def apiTest(requirementID, ws_path, repo_path, file_path):
        pass