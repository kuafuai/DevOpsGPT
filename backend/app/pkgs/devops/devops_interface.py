from abc import ABC, abstractmethod

from config import GRADE

class DevopsInterface(ABC):
    @abstractmethod
    def triggerPipeline(self, branchName, repoPath):
        pass

    @abstractmethod
    def getPipelineStatus(self, pipelineId, repoPath):
        pass

    @abstractmethod
    def getPipelineJobLogs(self, repopath, pipeline_id, job_id):
        pass