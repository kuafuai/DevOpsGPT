from app.models.app import App
from app.pkgs.knowledge.app_info_interface import AppInfoInterface

class AppInfoBasic(AppInfoInterface):
    def getAppArchitecture(self, appID):
        appID = int(appID)

        apps = App.getAll("")
        appArchitecture = ""
        for app in apps:
            if app["id"] == appID:
                services = app["service"]
                for service in services:
                    appArchitecture += service["intro"]+"\n\n"

        return appArchitecture.strip(), True
    
    def getServiceSwagger(self, appID, serviceName):
        appID = int(appID)

        apps = App.getAll("")
        swaggerDoc = ""
        for app in apps:
            if app["id"] == appID:
                services = app["service"]
                for service in services:
                    if service["name"] == serviceName:
                        swaggerDoc = service["api_doc"]
                    # todo Use llm to determine which interface documents to adjust
                    if len(service["api_doc"]) > 0:
                        swaggerDoc = service["api_doc"]

        return swaggerDoc, True

    def getServiceBasePrompt(self, appID, serviceName):
        appID = int(appID)

        apps = App.getAll("")
        appBasePrompt = ""
        for app in apps:
            if app["id"] == appID:
                services = app["service"]
                for service in services:
                    if service["name"] == serviceName:
                        appBasePrompt = service["base_prompt"]

        return appBasePrompt, True


    def getServiceIntro(self, appID, serviceName):
        appID = int(appID)

        apps = App.getAll("")
        appInfo = ""
        for app in apps:
            if app["id"] == appID:
                services = app["service"]
                for service in services:
                    if service["name"] == serviceName:
                        appInfo = service["intro"]

        return appInfo, True
    
    def getServiceLib(self, appID, serviceName):
        appID = int(appID)

        apps = App.getAll("")
        appLib = ""
        for app in apps:
            if app["id"] == appID:
                services = app["service"]
                for service in services:
                    if service["name"] == serviceName:
                        appLib = service["lib"]

        return appLib, True

    def getServiceStruct(self, appID, serviceName):
        appID = int(appID)

        apps = App.getAll("")
        projectStruct = ""
        for app in apps:
            if app["id"] == appID:
                services = app["service"]
                for service in services:
                    if service["name"] == serviceName:
                        projectStruct = service["struct"]

        return projectStruct, True

    def getServiceSpecification(self, appID, serviceName, LibName):
        appID = int(appID)

        apps = App.getAll("")
        coderequire = ""
        for app in apps:
            if app["id"] == appID:
                services = app["service"]
                for service in services:
                    if service["name"] == serviceName:
                        requires = service['specification']
                        if LibName in requires:
                            coderequire = requires[LibName]
        return coderequire, True

    def getServiceGitPath(self, appID, serviceName):
        appID = int(appID)

        apps = App.getAll("")
        gitPath = ""
        for app in apps:
            if app["id"] == appID:
                services = app["service"]
                for service in services:
                    if service["name"] == serviceName:
                        gitPath = service["git_path"]

        return gitPath, True
    
    def getServiceGitWorkflow(self, appID, serviceName):
        appID = int(appID)

        apps = App.getAll("")
        gitWorkflow = ""
        for app in apps:
            if app["id"] == appID:
                services = app["service"]
                for service in services:
                    if service["name"] == serviceName:
                        gitWorkflow = service["git_workflow"]

        return gitWorkflow, True
    
    def getServiceDockerImage(self, appID, serviceName):
        appID = int(appID)

        apps = App.getAll("")
        gitWorkflow = ""
        for app in apps:
            if app["id"] == appID:
                services = app["service"]
                for service in services:
                    if service["name"] == serviceName:
                        gitWorkflow = service["docker_image"]

        return gitWorkflow, True
    
    def getServiceDockerGroup(self, appID, serviceName):
        appID = int(appID)

        apps = App.getAll("")
        gitWorkflow = ""
        for app in apps:
            if app["id"] == appID:
                services = app["service"]
                for service in services:
                    if service["name"] == serviceName:
                        gitWorkflow = service["docker_group"]

        return gitWorkflow, True
    
    def getServiceDockerName(self, appID, serviceName):
        appID = int(appID)

        apps = App.getAll("")
        gitWorkflow = ""
        for app in apps:
            if app["id"] == appID:
                services = app["service"]
                for service in services:
                    if service["name"] == serviceName:
                        gitWorkflow = service["docker_name"]

        return gitWorkflow, True