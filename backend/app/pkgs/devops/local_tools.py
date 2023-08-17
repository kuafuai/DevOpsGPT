import subprocess
import platform
from app.pkgs.tools.utils_tool import detect_programming_language, get_last_n_lines
from app.pkgs.tools.file_tool import read_file_content
from config import WORKSPACE_PATH

def getFileContent(file_path, branch_name, repopath):
    path = WORKSPACE_PATH + repopath + "/" + file_path

    try:
        success, content = read_file_content(path)
        if not success:
            return False, ""
    except Exception as e:
        return False, ""

    return True, content 

def compileCheck(ws_path,repo_path):
    print("compile_check:")
    gitCwd = ws_path+'/'+repo_path
    print(gitCwd)

    if platform.system() == 'Windows':
        sub = ['build.cmd']
        result = subprocess.run(
            sub, capture_output=True, text=True, shell=True, cwd=gitCwd)
    else:
        sub = ['sh', 'build.sh']
        result = subprocess.run(
            sub, capture_output=True, text=True, cwd=gitCwd)

    print(result)
    if result.returncode != 0:
        stderr = get_last_n_lines(result.stderr, 20)
        if len(stderr)<5:
            stderr = get_last_n_lines(result.stdout, 20)
        return False, stderr
    return True, result.stdout

def lintCheck(ws_path, repo_path, file_path):
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
        return False, stderr
    return True, result.stdout