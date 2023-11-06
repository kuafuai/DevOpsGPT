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

REQUIREMENT_STATUS_NotStarted = "NotStarted"
REQUIREMENT_STATUS_InProgress = "InProgress"
REQUIREMENT_STATUS_Completed = "Completed"
REQUIREMENT_STATUS_Evaluated = "Evaluated"
REQUIREMENT_STATUS_Canceled = "Canceled"

REQUIREMENT_MEM_STEP_Requirement_clarify = "Requirement_clarify"
REQUIREMENT_MEM_STEP_Requirement_organize = "Requirement_organize"
REQUIREMENT_MEM_STEP_Requirement_adjust = "Requirement_adjust"
REQUIREMENT_MEM_STEP_Requirement_review = "Requirement_review"
REQUIREMENT_MEM_STEP_API_subtasks = "API_subtasks"
REQUIREMENT_MEM_STEP_API_organize = "API_organize"
REQUIREMENT_MEM_STEP_Subtask_chooseLib = "Subtask_chooseLib"
REQUIREMENT_MEM_STEP_Subtask_Subtask_genStruct = "Subtask_genStruct"
REQUIREMENT_MEM_STEP_Subtask_subtasks = "Subtask_subtasks"
REQUIREMENT_MEM_STEP_Subtask_pseudocode = "Subtask_pseudocode"
REQUIREMENT_MEM_STEP_Subtask_code = "Subtask_code"
REQUIREMENT_MEM_STEP_Code_checkCode = "Code_checkCode"
REQUIREMENT_MEM_STEP_Code_referenceRepair = "Code_referenceRepair"
REQUIREMENT_MEM_STEP_Code_analyzeError = "Code_analyzeError"
REQUIREMENT_MEM_STEP_Code_fixError = "Code_fixError"
REQUIREMENT_MEM_STEP_Code_reviewCode = "Code_reviewCode"
REQUIREMENT_MEM_STEP_Code_mergeCode = "Code_mergeCode"
REQUIREMENT_MEM_STEP_Code_genCode = "Code_genCode"
REQUIREMENT_MEM_STEP_DevOps_compileCheck = "DevOps_compileCheck"
REQUIREMENT_MEM_STEP_DevOps_lintCheck = "DevOps_lintCheck"
REQUIREMENT_MEM_STEP_DevOps_unitTest = "DevOps_unitTest"
REQUIREMENT_MEM_STEP_DevOps_apiTest = "DevOps_apiTest"
REQUIREMENT_MEM_STEP_DevOps_CI = "DevOps_CI"
REQUIREMENT_MEM_STEP_DevOps_CD = "DevOps_CD"

REQUIREMENT_MEM_TYPE_RequirementDocument = "RequirementDocument"
REQUIREMENT_MEM_TYPE_APIDocument = "APIDocument"
REQUIREMENT_MEM_TYPE_Subtask = "Subtask"
REQUIREMENT_MEM_TYPE_Code = "Code"
REQUIREMENT_MEM_TYPE_DevOps = "DevOps"

try:
    SITE_NAME = read_config("SITE_NAME")
    INVITATION_CODE = read_config("INVITATION_CODE")
    BACKEND_HOST = read_config("BACKEND_HOST")
    BACKEND_URL = read_config("BACKEND_URL")
    BACKEND_DEBUG = read_config("BACKEND_DEBUG")
    LANGUAGE = read_config("LANGUAGE")
    BACKEND_PORT = read_config("BACKEND_PORT")
    APP_SECRET_KEY = read_config("APP_SECRET_KEY")
    WORKSPACE_PATH = read_config("WORKSPACE_PATH")
    AICODER_ALLOWED_ORIGIN = json.loads(read_config("AICODER_ALLOWED_ORIGIN"))
    SQLALCHEMY_DATABASE_URI = read_config("SQLALCHEMY_DATABASE_URI")
    GPT_KEYS = json.loads(read_config("GPT_KEYS"))
    LLM_MODEL = read_config("LLM_MODEL")
    MODE = read_config("MODE")
    GRADE = read_config("GRADE")
    AUTO_LOGIN = read_config("AUTO_LOGIN")
    USERS = json.loads(read_config("USERS"))
    DEVOPS_TOOLS = read_config("DEVOPS_TOOLS")
    GIT_ENABLED = read_config("GIT_ENABLED")
    GIT_URL = read_config("GIT_URL")
    GIT_API = read_config("GIT_API")
    GIT_TOKEN = read_config("GIT_TOKEN")
    GIT_USERNAME = read_config("GIT_USERNAME")
    GIT_EMAIL = read_config("GIT_EMAIL")
    GITHUB_PROXY = read_config("GITHUB_PROXY")
    CD_TOOLS = read_config("CD_TOOLS")
    CD_ACCESS_KEY = read_config("CD_ACCESS_KEY")
    CD_SECRET_KEY = read_config("CD_SECRET_KEY")
    EMAIL_SERVER = read_config("EMAIL_SERVER")
    EMAIL_PORT = read_config("EMAIL_PORT")
    EMAIL_SSL = read_config("EMAIL_SSL")
    EMAIL_SENDER = read_config("EMAIL_SENDER")
    EMAIL_PASSWORD = read_config("EMAIL_PASSWORD")

    PAYPAL_MODE = read_config("PAYPAL_MODE")
    PAYPAL_ID = read_config("PAYPAL_ID")
    PAYPAL_SECRET = read_config("PAYPAL_SECRET")

    ALIPAY_SERVER = read_config("ALIPAY_SERVER")
    ALIPAY_ID = read_config("ALIPAY_ID")
    ALIPAY_PRIVATE_KEY = read_config("ALIPAY_PRIVATE_KEY")
    ALIPAY_PUBLIC_KEY = read_config("ALIPAY_PUBLIC_KEY")
except Exception as e:
    print(f"\033[91mError: Failed to read the configuration, please copy a new env.yaml from env.yaml.tpl and reconfigure it according to the documentation. Error in env.yaml: {str(e)}. 读取配置错误，请重新从 env.yaml.tpl 复制一个 env.yaml 进行配置后重启程序。 \033[0m")
    input("Press Enter to exit...")
    exit()