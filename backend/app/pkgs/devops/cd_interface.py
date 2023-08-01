from abc import ABC, abstractmethod

from config import GRADE

# todo finish CD and cloud services
class CDInterface(ABC):
    @abstractmethod
    def triggerPipeline(self, branchName, repoPath):
        pass

    @abstractmethod
    def getPipelineStatus(self, pipelineId, repoPath):
        pass

    @abstractmethod
    def getPipelineLogs(self, repopath, pipeline_id, job_id):
        pass