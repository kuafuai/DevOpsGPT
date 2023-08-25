from abc import ABC, abstractmethod

from config import GRADE

class SettingInterface(ABC):
    @abstractmethod
    def getGitConfigList(self, owner):
        pass

    @abstractmethod
    def getCIConfigList(self, owner):
        pass

    @abstractmethod
    def getCDConfigList(self, owner):
        pass