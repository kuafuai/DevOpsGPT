import time
from app.pkgs.knowledge.app_info_interface import AppInfoInterface
from app.pkgs.tools.i18b import getI18n
from app.models.application import Application
from app.models.sys_lib import SysLib

class AppInfoBasic(AppInfoInterface):    
    def getServiceLib(self, appID, serviceName):
        appID = int(appID)

        appLib = ""
        apps = Application.get_all_application(0, appID)
        if len(apps) > 0:
            services = apps[0]["service"]
            for service in services:
                if service["name"] == serviceName:
                    for lib in service["libs"]:
                        appLib += lib["sys_lib_name"]+"\n"

        return appLib, True

    def getServiceStruct(self, appID, serviceName):
        appID = int(appID)

        projectStruct = ""
        apps = Application.get_all_application(0, appID)
        if len(apps) > 0:
            services = apps[0]["service"]
            for service in services:
                if service["name"] == serviceName:
                    projectStruct = service["struct_cache"]

        return projectStruct, True

    def getServiceSpecification(self, appID, serviceName, LibName):
        appID = int(appID)

        lib = SysLib.get_lib_by_name(LibName)
        specification = ""
        if "purpose" in lib and "specification" in lib:
            specification = lib["purpose"] +", "+ lib["specification"]

        return specification, True
    
    def analyzeService(self, tenant_id, gitPath):
        time.sleep(2)
        _ = getI18n("controllers")
        reJson = {
            "name" : gitPath,
            "git_config_id": 0,
            "ci_config_id": 0,
            "cd_config_id": 0,
            "cd_container_name": "",
            "cd_container_group": "",
            "cd_region": "",
            "cd_public_ip": "",
            "cd_security_group": "",
            "cd_subnet": "",
            "git_path": gitPath,
            "git_workflow": "default.yaml",
            "role": gitPath,
            "struct_cache": "unkonwn",
            "language": "unkonwn",
            "framework": "unkonwn",
            "database": "unkonwn",
            "api_type": "swagger",
            "api_location": "",
            "service_libs_name": "no"
        }
        return reJson, True

    def repo_analyzer(self, type, repo, task_id):
        return "", False
