from abc import ABC, abstractmethod

from config import GRADE

class ApiInterface(ABC):
    @abstractmethod
    def clarifyAPI(self, userPrompt, apiDoc):
        pass