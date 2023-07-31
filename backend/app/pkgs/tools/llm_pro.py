from app.pkgs.tools.llm_interface import LLMInterface

class LLMPro(LLMInterface):
    def chatCompletion(self, context):
        # The current version does not support this feature
        return "", False