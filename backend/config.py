import json
import yaml


def read_config(key):
    file_path = "env.yaml"
    with open(file_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
        value = config.get(key)
    return value

BACKEND_HOST = read_config("BACKEND_HOST")
BACKEND_DEBUG = read_config("BACKEND_DEBUG")
LANGUAGE = read_config("LANGUAGE")
BACKEND_PORT = read_config("BACKEND_PORT")
APP_SECRET_KEY = read_config("APP_SECRET_KEY")
WORKSPACE_PATH = read_config("WORKSPACE_PATH")
AICODER_ALLOWED_ORIGIN = read_config("AICODER_ALLOWED_ORIGIN")
SQLALCHEMY_DATABASE_URI = read_config("SQLALCHEMY_DATABASE_URI")
DEMO_TASK_ID = read_config("DEMO_TASK_ID")
GPT_KEYS = json.loads(read_config("GPT_KEYS"))
LLM_MODEL = read_config("LLM_MODEL")
MODE = read_config("MODE")
GRADE = read_config("GRADE")
AUTO_LOGIN = read_config("AUTO_LOGIN")
USERS = json.loads(read_config("USERS"))
DEVOPS_TOOLS = read_config("DEVOPS_TOOLS")
APPS = json.loads(read_config("APPS"))
GITLAB_URL = read_config("GITLAB_URL")
GITLAB_CLONE_URL = read_config("GITLAB_CLONE_URL")
GITLAB_TOKEN = read_config("GITLAB_TOKEN")
