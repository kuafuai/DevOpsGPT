from app.pkgs.prompt.api_interface import ApiInterface

class ApiPro(ApiInterface):
    def clarifyAPI(self, userPrompt, apiDocUrl):
        # The current version does not support this feature
        return "", False