# Configure the interface information of openai and azure. If a certain type of interface is not needed, please completely delete the corresponding element (openai\azure). 
# 配置 openai 和 azure 的接口信息（替换 sk-xxxx 为你的 key），如果不需要某个类型的接口，请将对应的元素整个删除掉（openai\azure），【注意】数组中最后一个元素后面不要加逗号、您可能需要开启全局代理来访问API接口
GPT_KEYS: |
    {
        "openai": {
            "keys": [
                {"sk-xxxx": {"count": 0, "timestamp": 0}}
            ],
            "api_type": "open_ai",
            "api_base": "https://api.openai.com/v1",
            "api_version": "2020-11-07",
            "proxy": "None"
        }
        ,
        "azure": {
            "keys": [
                {"sk-xxxx": {"count": 0, "timestamp": 0}}
            ],
            "api_type": "azure",
            "api_base": "https://example-gpt.openai.azure.com/",
            "api_version": "2023-05-15",
            "deployment_id": "deployment-name",
            "proxy": "None"
        }
    }

# Configure the model used (do not use less than 16k token model), [note] openai plus members and API members are different, you opena plus member does not mean that you can use gpt4 model, specifically consult the official documentation of openai
# 配置使用的模型（不要使用小于16k token的模型），【注意】openai的plus会员和API会员是不同的，你开通了plus会员不代表可以用gpt4的模型，具体查阅openai的官方文档
LLM_MODEL: "gpt-3.5-turbo-16k-0613"  

LANGUAGE: 'en'  # en、zh
SITE_NAME: 'DevOpsGPT'
INVITATION_CODE: ''
FRONTEND_PORT: 8080
BACKEND_PORT: 8081
# The url that the back end allows cross-domain access (front-end access address)
# 后端允许跨域访问的url（前端访问地址）
AICODER_ALLOWED_ORIGIN: '["http://127.0.0.1:8080"]'
BACKEND_URL: 'http://127.0.0.1:8081'

BACKEND_HOST: '0.0.0.0'
BACKEND_DEBUG: true
APP_SECRET_KEY: 'Es*lsnGptDevOps'
WORKSPACE_PATH: './workspace/'
SQLALCHEMY_DATABASE_URI: 'sqlite:///../db/database.db'
MODE: "REAL" # FAKE、REAL
GRADE: "base"

CD_TOOLS: "local"  # local、aliyun Open source version only supports Alibaba Cloud 当前开源版只支持阿里云
CD_ACCESS_KEY: ""
CD_SECRET_KEY: ""

DEVOPS_TOOLS: "local" # local、gitlab、github  Please refer to the official documentation of the tool to learn how to use it. 请查阅相关工具的官方文档了解如何使用
GIT_ENABLED: true  # Whether to enable Git. If yes, pull code from Git(Note APPS.service.git_path configuration item). 是否开启Git，如果开启将从Git中拉代码（注意 APPS.service.git_path 配置项）
GIT_URL: "https://github.com"  # https://github.com、https://gitlab.com
GIT_API: "https://api.github.com" # https://api.github.com
GIT_TOKEN: "xxxx"   # Get from here https://github.com/settings/tokens、https://gitlab.com/-/profile/personal_access_tokens
GIT_USERNAME: "xxxx"
GIT_EMAIL: "xxxx@x.x"
GITHUB_PROXY: ""

EMAIL_SERVER: ""
EMAIL_PORT: ""
EMAIL_SSL: true
EMAIL_SENDER: ""
EMAIL_PASSWORD: ""

PAYPAL_MODE: "sandbox" # sandbox or live
PAYPAL_ID: "xxxx"
PAYPAL_SECRET: "xxxx"
ALIPAY_SERVER: "https://openapi-sandbox.dl.alipaydev.com/gateway.do" # sandbox or live
ALIPAY_ID: "666"
ALIPAY_PRIVATE_KEY: "xxxx"
ALIPAY_PUBLIC_KEY: "xxxx"

AUTO_LOGIN: true
USERS: |
  {
    "demo_user": "123456"
  }