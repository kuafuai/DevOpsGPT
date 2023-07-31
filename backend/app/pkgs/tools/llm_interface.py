from abc import ABC, abstractmethod

from config import GRADE

class LLMInterface(ABC):
    @abstractmethod
    def chatCompletion(self, context):
        pass