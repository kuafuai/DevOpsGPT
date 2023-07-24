# from app.models.app import App
# from app.pkgs.devops.local_tools import compile_check
from app.pkgs.tools.file_tool import read_file_content

if __name__ == '__main__':
    # compile_check("./workspace/demo-task/java_demo_backend/", "1")
    isSuccess, content = read_file_content("./workspace/demo-task/java_demo_backend/build.cmd")
    print(isSuccess, content)
