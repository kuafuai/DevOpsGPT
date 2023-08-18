import json
import yaml


def read_config(key):
    try:
        file_path = "env.yaml"
        with open(file_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
            value = config.get(key)
    except Exception as e:
        print(f"\033[91mError: Failed to read the {key} configuration, please copy a new env.yaml from env.yaml.tpl and reconfigure it according to the documentation. 读取配置错误，请重新从 env.yaml.tpl 复制一个 env.yaml 进行配置后重启程序。\033[0m")
        input("Press Enter to exit...")
        exit()
    if value is None:
        print(f"\033[91mError: Failed to read the {key} configuration, please copy a new env.yaml from env.yaml.tpl and reconfigure it according to the documentation. 读取配置错误，请重新从 env.yaml.tpl 复制一个 env.yaml 进行配置后重启程序。\033[0m")
        input("Press Enter to exit...")
        exit()

    return value

try:
    BACKEND_HOST = read_config("BACKEND_HOST")
    BACKEND_DEBUG = read_config("BACKEND_DEBUG")
    LANGUAGE = read_config("LANGUAGE")
    BACKEND_PORT = read_config("BACKEND_PORT")
    APP_SECRET_KEY = read_config("APP_SECRET_KEY")
    WORKSPACE_PATH = read_config("WORKSPACE_PATH")
    AICODER_ALLOWED_ORIGIN = read_config("AICODER_ALLOWED_ORIGIN")
    SQLALCHEMY_DATABASE_URI = read_config("SQLALCHEMY_DATABASE_URI")
    GPT_KEYS = json.loads(read_config("GPT_KEYS"))
    LLM_MODEL = read_config("LLM_MODEL")
    MODE = read_config("MODE")
    GRADE = read_config("GRADE")
    AUTO_LOGIN = read_config("AUTO_LOGIN")
    USERS = json.loads(read_config("USERS"))
    DEVOPS_TOOLS = read_config("DEVOPS_TOOLS")
    APPS = json.loads(read_config("APPS"))
    GIT_ENABLED = read_config("GIT_ENABLED")
    GIT_URL = read_config("GIT_URL")
    GIT_API = read_config("GIT_API")
    GIT_TOKEN = read_config("GIT_TOKEN")
    GIT_USERNAME = read_config("GIT_USERNAME")
    GIT_EMAIL = read_config("GIT_EMAIL")
    CD_TOOLS = read_config("CD_TOOLS")
    CD_ACCESS_KEY = read_config("CD_ACCESS_KEY")
    CD_SECRET_KEY = read_config("CD_SECRET_KEY")
    CD_REGION = read_config("CD_REGION")
    CD_EIP = read_config("CD_EIP")
    CD_SECURITY = read_config("CD_SECURITY")
    CD_SWITCH = read_config("CD_SWITCH")
except Exception as e:
    print(f"\033[91mError: Failed to read the configuration, please copy a new env.yaml from env.yaml.tpl and reconfigure it according to the documentation. Error in env.yaml: {str(e)}. 读取配置错误，请重新从 env.yaml.tpl 复制一个 env.yaml 进行配置后重启程序。 \033[0m")
    input("Press Enter to exit...")
    exit()