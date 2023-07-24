import subprocess
import platform
import os
from app.pkgs.tools.utils_tool import detect_programming_language, get_last_n_lines
from app.pkgs.tools.file_tool import read_file_content
from config import WORKSPACE_PATH

def get_file_content(file_path, branch_name, repopath):
    path = WORKSPACE_PATH + repopath + "/" + file_path

    try:
        success, content = read_file_content(path)
        if not success:
            return False, ""
    except Exception as e:
        return False, ""

    return True, content 

def trigger_pipeline(branch_name, repopath):
    return "The pipeline cannot be run locally now, you can view the configuration and select tools such as gitlab.", 0, "", False

def compile_check(ws_path,repo_path):
    print("compile_check:")
    print(ws_path)

    if platform.system() == 'Windows':
        sub = ['build.cmd']
        result = subprocess.run(
            sub, capture_output=True, text=True, shell=True, cwd=ws_path)
    else:
        sub = ['sh', 'build.sh']
        result = subprocess.run(
            sub, capture_output=True, text=True, cwd=ws_path)

    print(result)
    if result.returncode != 0:
        stderr = get_last_n_lines(result.stderr, 20)
        if len(stderr)<5:
            stderr = get_last_n_lines(result.stdout, 20)
        return False, stderr
    return True, result.stdout

def lint_check(ws_path, repo_path, file_path):
    print("check_lint:"+ws_path)
    if detect_programming_language(file_path) == "Python":
        result = subprocess.run(
            ['pylint', '--disable=all', '--enable=syntax-error', file_path], capture_output=True, text=True, cwd=ws_path)
    else:
        return True, "Code Scan PAAS."
        
    print("lint_check:")
    print(ws_path)
    print(result)
    if result.returncode != 0:
        stderr = get_last_n_lines(result.stderr, 20)
        if len(stderr)<5:
            stderr = get_last_n_lines(result.stdout, 20)
        return False, stderr
    return True, result.stdout