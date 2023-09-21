from app.pkgs.tools import storage
from app.models.setting_interface import SettingInterface
from app.pkgs.tools.utils_tool import hide_half_str
from config import DEVOPS_TOOLS, GIT_URL, GIT_TOKEN, GIT_USERNAME, GIT_EMAIL, GIT_API, CD_TOOLS, CD_ACCESS_KEY, CD_SECRET_KEY, GPT_KEYS

class SettingBasic(SettingInterface):
    def getGitConfigList(self, tenantID, appID, hideToken = False):
        gitList = []
        name = "Public git config"
        if storage.get("language") == 'zh':
            name = "公共Git配置"
        public_cfg = {
            "name" : name,
            "git_provider" : DEVOPS_TOOLS,
            "git_url" : GIT_URL,
            "git_token" : GIT_TOKEN,
            "git_config_id" : 0,
            "git_username" : GIT_USERNAME,
            "git_email" : GIT_EMAIL
        }
        if hideToken:
            public_cfg["git_token"] = hide_half_str(public_cfg["git_token"])
       
        gitList.append(public_cfg)

        return gitList, True
    
    def getCIConfigList(self, tenantID, appID, hideToken=False):
        gitList = []
        name = "Public CI config"
        if storage.get("language") == 'zh':
            name = "公共CI配置"
        public_cfg = {
            "name" : name,
            "ci_provider" : DEVOPS_TOOLS,
            "ci_config_id" : 0,
            "ci_api_url" : GIT_API,
            "git_url" : GIT_URL,
            "ci_token" : GIT_TOKEN
        }
        if hideToken:
            public_cfg["ci_token"] = hide_half_str(public_cfg["ci_token"])
        
        gitList.append(public_cfg)

        return gitList, True
    
    def getCDConfigList(self, tenantID, appID, hideToken):
        gitList = []
        name = "Public CD config"
        if storage.get("language") == 'zh':
            name = "公共CD配置"
        public_cfg = {
            "name" : name,
            "cd_provider" : CD_TOOLS,
            "ACCESS_KEY" : CD_ACCESS_KEY,
            "SECRET_KEY" : CD_SECRET_KEY,
            "cd_config_id" : 0
        }
        if hideToken:
            public_cfg["ACCESS_KEY"] = hide_half_str(public_cfg["ACCESS_KEY"])
            public_cfg["SECRET_KEY"] = hide_half_str(public_cfg["SECRET_KEY"])

        gitList.append(public_cfg)

        return gitList, True
    
    def getLLMConfigList(self, tenantID, appID):
        gptKeys = GPT_KEYS
        gitList = []

        for key in gptKeys["openai"]["keys"]:
            for keykey in key:
                print(keykey)
            gitList.append({
                "llm_config_id" : 0,
                "llm_provider" : gptKeys["openai"]["api_type"],
                "llm_api_url" : gptKeys["openai"]["api_base"],
                "llm_api_version" : gptKeys["openai"]["api_version"],
                "llm_api_proxy" : gptKeys["openai"]["proxy"],
                "llm_key": keykey
            })

        return gitList, True