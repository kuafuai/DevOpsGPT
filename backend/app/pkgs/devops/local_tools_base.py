import subprocess
import platform
from app.pkgs.tools.utils_tool import detect_programming_language, get_last_n_lines
from app.pkgs.devops.local_tools_interface import LocalToolsInterface
from config import WORKSPACE_PATH

class LocalToolsBase(LocalToolsInterface):
    def compileCheck(self, requirementID, ws_path, repo_path):
        print("compile_check:")
        gitCwd = ws_path+'/'+repo_path
        script = ""
        print(gitCwd)

        if platform.system() == 'Windows':
            script = "build.cmd"
            sub = [script]
            result = subprocess.run(
                sub, capture_output=True, text=True, shell=True, cwd=gitCwd)
        else:
            script = "build.sh"
            sub = ['sh', script]
            result = subprocess.run(
                sub, capture_output=True, text=True, cwd=gitCwd)

        print(result)
        if result.returncode != 0:
            stderr = get_last_n_lines(result.stderr, 20)
            if len(stderr)<5:
                stderr = get_last_n_lines(result.stdout, 20)
            success = False
            re = stderr
        else:
            success = True
            re = result.stdout

        return success, re

    def lintCheck(self, requirementID, ws_path, repo_path, file_path):
        if detect_programming_language(file_path) == "Python":
            result = subprocess.run(
                ['pylint', '--disable=all', '--enable=syntax-error', f"{repo_path}/{file_path}"], capture_output=True, text=True, cwd=ws_path)
        else:
            return True, "Code Scan PAAS."
            
        print("lint_check:")
        print(ws_path)
        print(result)
        if result.returncode != 0:
            stderr = get_last_n_lines(result.stderr, 20)
            if len(stderr)<5:
                stderr = get_last_n_lines(result.stdout, 20)
            success = False
            re = stderr
        else:
            success = True
            re = result.stdout
        
        return success, re
    
    def unitTest(self, requirementID, ws_path, repo_path, file_path):
        return True, "The current version does not support this feature"
    
    def apiTest(self, requirementID, ws_path, repo_path, file_path):
        return True, "The current version does not support this feature"