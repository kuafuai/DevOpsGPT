from app.pkgs.prompt.requirement_interface import RequirementInterface


class RequirementPro(RequirementInterface):
    def clarifyRequirementPro(self, userPrompt, globalContext, appArchitecture):
        # The current version does not support this feature
        return [], False
