# Quick Start

1. Clone the latest code or select a released version.
2. Generate the configuration file: Copy `env.yaml.tpl` and rename it to `env.yaml`.
3. Modify the configuration file: Edit `env.yaml` and add the necessary information such as GPT Token .
4. Run the service: Execute `sh run.sh` on Linux or Mac, or double-click `run.bat` on Windows.
5. Access the service: Access the service through a browser (check the startup log for the access address, default is http://127.0.0.1:8080).
6. Complete requirement development: Follow the instructions on the page to complete requirement development, and view the generated code in the `./workspace` directory.

# Configuration Details

### Basic Configuration

1. FRONTEND_PORT, BACKEND_PORT: Frontend and backend ports.
2. AICODER_ALLOWED_ORIGIN: Allowed cross-origin addresses for the backend, matching the frontend's access address. Note: If you're not accessing the website via 127.0.0.1, manually modify `apiUrl` in frontend/static/js/coder.js.
3. LANGUAGE: Language.
4. LLM_MODEL: Model.
5. GPT_KEYS: Keys for GPT, configure OpenAI and Azure API information (replace sk-xxxx with your key). If you don't need a certain type of API, delete the corresponding element entirely (openai/azure). Note: Do not add a comma after the last element in the array. You might need to use a global proxy to access the API.
6. USERS: Login user configuration.

### Git Configuration

DevOpsGPT supports integration with Git. When enabled, development tasks can pull and push code from Git.

1. GIT_ENABLED: Enable Git.
2. GIT_URL: Configure your Git address, e.g., https://github.com, https://gitlab.com.
3. GIT_TOKEN: Configure your Git token, obtainable from here: https://github.com/settings/tokens, https://gitlab.com/-/profile/personal_access_tokens.
4. GIT_USERNAME: Git login username.
5. GIT_EMAIL: Git email.
6. APPS.service.git_path: Git path corresponding to the application, including the group, e.g., kuafuai/template_freestyleApp.

### CI/CD Tool Configuration

DevOpsGPT supports integration with CI tools like GitlabCI, GithubActions, etc., triggering your pipeline upon code submission.

<img src="files/ci.png" width="80%">

1. Complete the "Git Configuration" section above.
2. GIT_API: Configure the Git API address, e.g., https://api.github.com.
3. If using Gitlab, set up the pipeline, e.g., [.gitlab-ci.yml](https://github.com/kuafuai/template_javaWebApp_backend/blob/master/.gitlab-ci.yml). Also, configure Gitlab runner in Gitlab, details in the [Gitlab documentation](https://docs.gitlab.com/runner/).
4. If using Github, set up the pipeline, e.g., [default.yaml](https://github.com/kuafuai/template_javaWebApp_backend/blob/master/.github/workflows/default.yaml). Refer to the [Github documentation](https://docs.github.com/en/actions/learn-github-actions) for details.

### APPS Configuration

APPS contains information about the applications you need to develop. The first step in using the product is selecting a development application. During development, this information guides how the application should be designed and developed. In the open-source version, this information needs to be maintained manually. We'll provide AI intelligent analysis to automatically generate relevant information in the commercial version.

- app: Application, including multiple services like backend, frontend, microservices.
- name, intro: Display purposes only.
- service.name: Service name, must be unique.
- service.git_workflow: Github workflow name, effective only when Github CI is enabled.
- service.git_path: Git path, should include group, e.g., kuafuai/template_freestyleApp.
- service.base_prompt: Basic starting prompt, affects task development effectiveness.
- service.intro: Basic information about the service.
  - setpReqChooseLib (analysis of libraries/packages used together with service information).
- service.api_doc_url: API documentation URL, used to dynamically retrieve API documentation.
- service.api_doc: Current API documentation.
- service.struct: File directory structure information for the service.
  - setp1Task (used for breaking down tasks).
- service.lib: Libraries/packages available for the service.
  - setpReqChooseLib (analysis of libraries/packages used together).
- service.specification: Specification for using library packages.