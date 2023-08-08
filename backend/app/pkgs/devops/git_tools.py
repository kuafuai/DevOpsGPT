import subprocess

import gitlab
from config import GIT_TOKEN, GIT_URL, GIT_USERNAME
from config import WORKSPACE_PATH

def pullCode(ws_path, repo_path, base_branch, feature_branch):    
    result = subprocess.run(
        ['mkdir', '-p', ws_path], capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr)
        return False, result.stderr

    gitUrl = genCloneUrl(repo_path)
    print(f"pullCode start {gitUrl} {base_branch} {repo_path} {ws_path}")
    result = subprocess.run(['git', 'clone', '-b', base_branch, gitUrl, repo_path], capture_output=True, text=True, cwd=ws_path)
    if result.returncode != 0:
        print(result.stderr)
        return False, result.stderr

    result = subprocess.run(
        ['git', 'checkout', '-b', feature_branch], capture_output=True, text=True, cwd=ws_path+'/'+repo_path)
    if result.returncode != 0:
        print(result.stderr)
        return False, result.stderr

    print(f"Code clone success. in {ws_path}")
    return True, f"Code clone success. in {ws_path}"
    
def pushCode(wsPath, gitPath, fatureBranch, commitMsg):
    gitCwd = wsPath+'/'+gitPath

    result = subprocess.run(
        ['git', 'add', '.'], capture_output=True, text=True, cwd=gitCwd)
    if result.returncode != 0:
        print(result.stderr)
        return False, result.stderr
    
    result = subprocess.run(
        ['git', 'commit', '-m', commitMsg], capture_output=True, text=True, cwd=gitCwd)
    if result.returncode != 0:
        print(result.stderr)
        return False, result.stderr

    gitUrl = genCloneUrl(gitPath)
    print(f"pushCode start {gitUrl} {fatureBranch} {gitPath} {wsPath}")
    result = subprocess.run(
        ['git', 'push', 'origin', fatureBranch], capture_output=True, text=True, cwd=gitCwd)
    if result.returncode != 0:
        print(result.stderr)
        return False, result.stderr

    print(f"push code success. in {wsPath}")
    return True, f"push code success. in {wsPath}"
    
def genCloneUrl(gitPath):
    # Extract the domain from the giturl
    domain = GIT_URL.split("//")[1]

    # Combine the components to form the final URL
    finalUrl = f"https://{GIT_USERNAME}:{GIT_TOKEN}@{domain}/{gitPath}.git"

    return finalUrl