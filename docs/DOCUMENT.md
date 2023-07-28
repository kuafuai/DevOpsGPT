## Quick Start

1. Clone the latest code or select a released version.
2. Generate the configuration file: Copy `env.yaml.tpl` and rename it to `env.yaml`.
3. Modify the configuration file: Edit `env.yaml` and add the necessary information such as GPT Token (refer to [documentation link](DOCUMENT.md) for detailed instructions).
4. Run the service: Execute `sh run.sh` on Linux or Mac, or double-click `run.bat` on Windows.
5. Access the service: Access the service through a browser (check the startup log for the access address, default is http://127.0.0.1:8080).
6. Complete requirement development: Follow the instructions on the page to complete requirement development, and view the generated code in the `./workspace` directory.

For detailed documentation and configuration parameters, please refer to the [documentation link](DOCUMENT.md).

## Config Parameters Explanation

### Basic Configuration Class
1. FRONTEND_PORT/BACKEND_PORT: The frontend and backend ports.
2. LANGUAGE: The language used.
3. LLM_MODEL: The model being used.
4. GPT_KEYS: Tokens for GPT.
5. USERS: Configuration for login users.

### APP Configuration
The "app" refers to the chosen development application. The first step in using the product is to select a specific development application.

- name/intro: Some display information for the frontend.
- project.project_base_prompt: The basic prompt for coding in the project.
- project.project_info: Basic project information, such as the development language, framework, and other relevant details.
- project.project_struct: The project's directory structure.
- project.project_lib: Components used in the project, such as Gson, OkHttp, etc.
- project.project_code_require: Requirements for coding with project components, for example, using the Lombok plugin to simplify code.

## 快速开始

1. 克隆最新代码或选择已发布的版本。
2. 生成配置文件：复制 `env.yaml.tpl` 并重命名为 `env.yaml`。
3. 修改配置文件：编辑 `env.yaml`，添加GPT Token等必要信息（详细说明请参考[文档链接](DOCUMENT.md)）。
4. 运行服务：在 Linux 或 Mac 上执行 `sh run.sh`，在 Windows 上双击运行 `run.bat`。
5. 访问服务：通过浏览器访问服务（启动日志中提供的访问地址，默认为 http://127.0.0.1:8080）。
6. 完成需求开发：按照页面引导完成需求开发，在 `./workspace` 目录下查看生成的代码。

详细文档和配置参数请参考[文档链接](DOCUMENT.md)。

## 配置文件参数说明

### 基础配置类

1. FRONTEND_PORT/BACKEND_PORT ：前端端口和后端端口
2. LANGUAGE：语言
3. LLM_MODEL：模型
4. GPT_KEYS：GPT的token
5. USERS：登录用户配置

### APP配置
app是选择开发的应用。在使用产品的第一步就是选择某个开发应用

- name/intro：前端一些展示信息
- project.project_base_prompt：项目写代码的基础prompt
- project.project_info：项目基本信息；比如开发语言、开发框架等一些信息
- project.project_struct：项目目录结构
- project.project_lib：项目中使用的组件；比如Gson、OkHttp等
- project.project_code_require：项目组件写代码的要求；比如使用Lombok插件简化代码等
