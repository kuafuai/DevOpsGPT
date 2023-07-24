from app.models.app import App


def getSwagger(apiDocUrl):
    apps = App.getAll("")
    swaggerDoc = ""
    for app in apps:
        if app["api_doc_url"] == apiDocUrl:
            swaggerDoc = app["api_doc"]

    return swaggerDoc, True


def getServiceStruct(apiDocUrl):
    apps = App.getAll("")
    serviceStructure = ""
    for app in apps:
        if app["api_doc_url"] == apiDocUrl:
            serviceStructure = app["service_structure"]

    return serviceStructure, True


def getProjectBasePrompt(apiDocUrl):
    apps = App.getAll("")
    appBasePrompt = ""
    for app in apps:
        if app["api_doc_url"] == apiDocUrl:
            project = app["project"]
            appBasePrompt = project["project_base_prompt"]

    return appBasePrompt, True


def getProjectAppInfo(apiDocUrl):
    apps = App.getAll("")
    appInfo = ""
    for app in apps:
        if app["api_doc_url"] == apiDocUrl:
            project = app["project"]
            appInfo = project["project_info"]

    return appInfo, True

def getProjectStruct(apiDocUrl):
    apps = App.getAll("")
    projectStruct = ""
    for app in apps:
        if app["api_doc_url"] == apiDocUrl:
            project = app["project"]
            projectStruct = project["project_struct"]

    return projectStruct, True

def getProjectLib(apiDocUrl):
    apps = App.getAll("")
    appLib = ""
    for app in apps:
        if app["api_doc_url"] == apiDocUrl:
            project = app["project"]
            appLib = project["project_lib"]

    return appLib, True

def getProjectCoderequire(apiDocUrl, name):
    apps = App.getAll("")
    coderequire = ""
    for app in apps:
        if app["api_doc_url"] == apiDocUrl:
            project = app["project"]
            requires = project['project_code_require']
            if name in requires:
                coderequire = requires[name]
    return coderequire, True

