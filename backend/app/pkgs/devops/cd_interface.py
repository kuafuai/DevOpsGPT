from abc import ABC, abstractmethod

# todo finish CD and cloud services
class CDInterface(ABC):
    @abstractmethod
    def triggerCD(self, image, container_grpup, container_name, cdConfigList):
        pass