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
FRONTEND_PORT: 8080
BACKEND_PORT: 8081
# The url that the back end allows cross-domain access (front-end access address)
# 后端允许跨域访问的url（前端访问地址）
AICODER_ALLOWED_ORIGIN: 'http://127.0.0.1:8080'  

BACKEND_HOST: '0.0.0.0'
BACKEND_DEBUG: true
APP_SECRET_KEY: 'Es*lsnGptDevOps'
WORKSPACE_PATH: './workspace/'
SQLALCHEMY_DATABASE_URI: 'sqlite:///app.db'
MODE: "REAL" # FAKE、REAL
GRADE: "base"

CD_TOOLS: "local"  # local、aliyun Open source version only supports Alibaba Cloud 当前开源版只支持阿里云
CD_ACCESS_KEY: ""
CD_SECRET_KEY: ""
CD_REGION: "cn-hongkong" # region 部署地域
CD_EIP: "eip-xxx" # Public IP address 公网IP，用于访问公网
CD_SECURITY: "sg-xxx" # Security group 安全组，用于开放容器端口
CD_SWITCH: "vsw-xxx" # switch 交换机

DEVOPS_TOOLS: "local" # local、gitlab、github  Please refer to the official documentation of the tool to learn how to use it. 请查阅相关工具的官方文档了解如何使用
GIT_ENABLED: true  # Whether to enable Git. If yes, pull code from Git(Note APPS.service.git_path configuration item). 是否开启Git，如果开启将从Git中拉代码（注意 APPS.service.git_path 配置项）
GIT_URL: "https://github.com"  # https://github.com、https://gitlab.com
GIT_API: "https://api.github.com" # https://api.github.com
GIT_TOKEN: "xxxx"   # Get from here https://github.com/settings/tokens、https://gitlab.com/-/profile/personal_access_tokens
GIT_USERNAME: "xxxx"
GIT_EMAIL: "xxxx@x.x"

AUTO_LOGIN: true
USERS: |
  {
    "demo_user": "123456"
  }

APPS: |
  [
    {
        "id": 3,
        "name": "Demo applications that support any development needs（支持任何开发需求的演示应用）",
        "intro": "Demo applications that support any development needs, You can submit any development requirements.",
        "default_source_branch": "master",
        "default_target_branch": "dev",
        "service": [
            {
                "name": "free_demo",
                "git_path": "kuafuai/template_freestyleApp",
                "git_workflow": "default.yaml",
                "docker_image": "docker.io/kuafuai/template-freestyleapp:latest",
                "docker_group": "devopsgtp-test",
                "docker_name": "free-demo",
                "base_prompt": "You can choose any appropriate development language",
                "intro": "service name: free_demo\nrole of service: used to develop any requirements\ndevelopment language: no limit\ndevelopment framework: no limit",
                "api_doc_url": "",
                "api_doc": "",
                "struct": "This is a new service, no limits",
                "lib": "no limit",
                "specification": {
                    "Default": "- You can choose any appropriate development language"
                }
            }
        ]
    },
    {
        "id": 2,
        "name": "Demo application with python+html front-end and back-end separation（前后端分离应用python+html）",
        "intro": "This is a python+html front-end and back-end separation application, back-end use python flask, front-end use html+jquery+semantic-ui. Front-end and back-end define interaction interfaces through Swagger documentation.",
        "default_source_branch": "master",
        "default_target_branch": "dev",
        "service": [
            {
                "name": "python_demo",
                "git_path": "kuafuai/template_pythonWebApp",
                "git_workflow": "default.yaml",
                "docker_image": "docker.io/kuafuai/template-pythonwebapp:latest",
                "docker_group": "devopsgtp-test",
                "docker_name": "python-demo",
                "base_prompt": "You need to develop both front-end and back-end code",
                "intro": "service name: python_demo\nrole of service: used to develop front-end and back-end requirements\ndevelopment language: python and html\ndevelopment framework: flask and jquery+semantic-ui",
                "api_doc_url": "2",
                "api_doc": "{\"swagger\":\"2.0\",\"info\":{\"description\":\"API documentation for AI Assistant\",\"version\":\"1.0\",\"title\":\"AI Assistant API Documentation\",\"contact\":{\"name\":\"AI Assistant\",\"url\":\"www.xxx.com\",\"email\":\"xxx@xxx.com\"}},\"host\":\"localhost:8086\",\"basePath\":\"/\"}",
                "struct": "- dir: backend, description:Back-end service directory\n- dir: frontend, description:Front-end service directory",
                "lib": "- flask(python Web framework)\n- jquery(JavaScript library)\n- semantic-ui(User interface library)\n- openai(chatgpt sdk)",
                "specification": {
                    "name": "python_demo",
                    "flask": "- python uses flask to provide web services",
                    "jquery": "- js uses the jQuery framework",
                    "openai": "- sdk for openai's chatgpt",
                    "semantic-ui": "- The front page uses the semantic-ui style library",
                    "Default": "- You need to develop both front-end and back-end code"
                }
            }
        ]
    },
    {
        "id": 1,
        "name": "Demo application with java+html front-end and back-end separation（前后端分离应用java+html）",
        "intro": "This is a java+html front-end and back-end separation project, back-end 'java_demo_backend' use spring mvc framework, front-end 'java_demo_frontend' use html+jquery+semantic-ui. Front-end and back-end define interaction interfaces through Swagger documentation.",
        "default_source_branch": "master",
        "default_target_branch": "feat/xxx",
        "service": [
            {
                "name": "java_demo_backend",
                "git_path": "kuafuai/template_javaWebApp_backend",
                "git_workflow": "default.yaml",
                "docker_image": "docker.io/kuafuai/template-javawebapp-backend:latest",
                "docker_group": "devopsgtp-test",
                "docker_name": "java-demo-backend",
                "base_prompt": "这是一个前后端分离的项目，你只负责后端接口的开发。作为一个资深JAVA系统架构师，基于MVC设计框架并使用Spring Boot和MyBatis3作为开发框架的Java项目中进行开发",
                "intro": "service name: java_demo_backend\nrole of service: used to develop back-end requirements\ndevelopment language: Java\ndevelopment framework: SpringBoot+Mybatis3\ndatabase: SQLite",
                "api_doc_url": "1",
                "api_doc": "{\"swagger\":\"2.0\",\"info\":{\"description\":\"API documentation for AI Assistant\",\"version\":\"1.0\",\"title\":\"AI Assistant API Documentation\",\"contact\":{\"name\":\"AI Assistant\",\"url\":\"www.xxx.com\",\"email\":\"xxx@xxx.com\"}},\"host\":\"localhost:8086\",\"basePath\":\"/\",\"tags\":[{\"name\":\"TargetController\",\"description\":\"Target Controller\"}],\"paths\":{\"/addTarget\":{\"post\":{\"tags\":[\"TargetController\"],\"summary\":\"Add a new target\",\"operationId\":\"addTargetUsingPOST\",\"consumes\":[\"application/json\"],\"produces\":[\"*/*\"],\"parameters\":[{\"in\":\"body\",\"name\":\"target\",\"description\":\"target\",\"required\":true,\"schema\":{\"$ref\":\"#/definitions/Target\"}}],\"responses\":{\"200\":{\"description\":\"OK\",\"schema\":{\"$ref\":\"#/definitions/ResultModel\"}},\"201\":{\"description\":\"Created\"},\"401\":{\"description\":\"Unauthorized\"},\"403\":{\"description\":\"Forbidden\"},\"404\":{\"description\":\"Not Found\"}},\"deprecated\":false}},\"/getTargetList\":{\"get\":{\"tags\":[\"TargetController\"],\"summary\":\"Get target list\",\"operationId\":\"getTargetListUsingGET\",\"produces\":[\"*/*\"],\"responses\":{\"200\":{\"description\":\"OK\",\"schema\":{\"$ref\":\"#/definitions/ResultPageModel«Target»\"}},\"401\":{\"description\":\"Unauthorized\"},\"403\":{\"description\":\"Forbidden\"},\"404\":{\"description\":\"Not Found\"}},\"deprecated\":false}}},\"definitions\":{\"Exception\":{\"type\":\"object\",\"properties\":{\"cause\":{\"$ref\":\"#/definitions/Throwable\"},\"localizedMessage\":{\"type\":\"string\"},\"message\":{\"type\":\"string\"},\"stackTrace\":{\"type\":\"array\",\"items\":{\"$ref\":\"#/definitions/StackTraceElement\"}},\"suppressed\":{\"type\":\"array\",\"items\":{\"$ref\":\"#/definitions/Throwable\"}}},\"title\":\"Exception\"},\"ResultModel\":{\"type\":\"object\",\"properties\":{\"code\":{\"type\":\"integer\",\"format\":\"int32\"},\"data\":{\"type\":\"object\"},\"exception\":{\"$ref\":\"#/definitions/Exception\"},\"msg\":{\"type\":\"string\"}},\"title\":\"ResultModel\"},\"ResultPageModel«Target»\":{\"type\":\"object\",\"properties\":{\"firstIndex\":{\"type\":\"integer\",\"format\":\"int32\"},\"list\":{\"type\":\"array\",\"items\":{\"$ref\":\"#/definitions/Target\"}},\"pageNo\":{\"type\":\"integer\",\"format\":\"int32\"},\"pageSize\":{\"type\":\"integer\",\"format\":\"int32\"},\"totalPage\":{\"type\":\"integer\",\"format\":\"int32\"},\"totalRecords\":{\"type\":\"integer\",\"format\":\"int32\"}},\"title\":\"ResultPageModel«Target»\"},\"StackTraceElement\":{\"type\":\"object\",\"properties\":{\"className\":{\"type\":\"string\"},\"fileName\":{\"type\":\"string\"},\"lineNumber\":{\"type\":\"integer\",\"format\":\"int32\"},\"methodName\":{\"type\":\"string\"},\"nativeMethod\":{\"type\":\"boolean\"}},\"title\":\"StackTraceElement\"},\"Target\":{\"type\":\"object\",\"properties\":{\"id\":{\"type\":\"integer\",\"format\":\"int32\"},\"targetName\":{\"type\":\"string\"},\"targetType\":{\"type\":\"string\"}},\"title\":\"Target\"},\"Throwable\":{\"type\":\"object\",\"properties\":{\"cause\":{\"$ref\":\"#/definitions/Throwable\"},\"localizedMessage\":{\"type\":\"string\"},\"message\":{\"type\":\"string\"},\"stackTrace\":{\"type\":\"array\",\"items\":{\"$ref\":\"#/definitions/StackTraceElement\"}},\"suppressed\":{\"type\":\"array\",\"items\":{\"$ref\":\"#/definitions/Throwable\"}}},\"title\":\"Throwable\"}}}",
                "struct": "- dir:src/main/resources/db/migration,description:flyway数据库版本管理sql脚本文件,新增和修改表字段\n- dir:src/main/java/com/aiassistant/model,description:数据库字段映射实体类\n- dir:src/main/java/com/aiassistant/mapper,description:定义数据库交互Mapper接口\n- dir:src/main/resources/mapper,description:文件类型是xml，是数据库操作SQL语句与Mapper的映射\n- dir:src/main/java/com/aiassistant/service,description:业务层Service接口定义\n- dir:src/main/java/com/aiassistant/service/impl,description:业务层Service接口具体实现\n- dir:src/main/java/com/aiassistant/controller,description:对外服务接口\n- dir:src/main/java/com/aiassistant/utils,description:通用工具类目录",
                "lib": "- Lombok\n- OkHttp\n- Jsoup\n- Gson\n- Flyway\n- MyBatis3",
                "specification": {
                    "MyBatis3": "- Sql脚本文件命名规则 VyyyymmddHHMM__description.sql，例如：V202307081234__create_target.sql。",
                    "Flyway": "- Sql脚本文件命名规则 VyyyymmddHHMM__description.sql，例如：V202307081234__create_target.sql。",
                    "SQLite": "- Sql脚本要符合SQLite语法。",
                    "OkHttp": "- 使用OkHttp组件，已经引入项目，不考虑导入依赖。",
                    "Gson": "- 使用Gson组件，已经引入项目，不考虑导入依赖。",
                    "Jsoup": "- 使用Jsoup组件，已经引入项目，不考虑导入依赖。",
                    "Default": "- 使用Spring开发范式。\n- 在即有项目中开发，不考虑项目配置。\n- 注意Java文件的package引用。\n- 使用Lombok插件简化代码。"
                }
            },
            {
                "name": "java_demo_frontend",
                "git_path": "kuafuai/template_javaWebApp_frontend",
                "git_workflow": "default.yaml",
                "docker_image": "docker.io/kuafuai/template-javawebapp-frontend:latest",
                "docker_group": "devopsgtp-test",
                "docker_name": "java-demo-frontend",
                "base_prompt": "这是一个前后端分离的项目，你只负责前端功能的开发，接口和数据库处理已经由后端实现，你可以直接调用",
                "intro": "service name: java_demo_frontend\nrole of service: used to develop frontend-end requirements\ndevelopment_language: html+js\ndevelopment_framework: jquery+semantic-ui",
                "api_doc_url": "",
                "api_doc": "",
                "struct": "- dir:html,description:html files\n- dir:js,description:JavaScript files\n- dir:css,description:css files",
                "lib": "- Semantic-ui\n- jQuery",
                "specification": {
                    "Semantic-ui": "- use Semantic-ui frontend framework",
                    "jQuery": "- use jQuery framework",
                    "Default": "- Make sure the page looks good"
                }
            }
        ]
    }
  ]