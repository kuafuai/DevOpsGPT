import os
import subprocess
from config import GIT_TOKEN, GIT_URL, GIT_USERNAME, GIT_EMAIL

def pullCode(ws_path, repo_path, base_branch, feature_branch):
    try:
        os.makedirs(ws_path, exist_ok=True)
    except Exception as e:
        return False, "mkdir failed: "+str(e)

    gitUrl = genCloneUrl(repo_path)
    print(f"pullCode start {gitUrl} {base_branch} {repo_path} {ws_path}")
    result = subprocess.run(['git', 'clone', '-b', base_branch, gitUrl, repo_path], capture_output=True, text=True, cwd=ws_path)
    if result.returncode != 0:
        print(result.stderr)
        return False, "git clone failed: "+result.stderr

    result = subprocess.run(
        ['git', 'checkout', '-b', feature_branch], capture_output=True, text=True, cwd=ws_path+'/'+repo_path)
    if result.returncode != 0:
        print(result.stderr)
        return False, "git checkout branch failed: "+result.stderr

    print(f"Code clone success. in {ws_path}")
    return True, f"Code clone success. in {ws_path}"
    
def pushCode(wsPath, gitPath, fatureBranch, commitMsg):
    gitCwd = wsPath+'/'+gitPath

    subprocess.run(
        ['git', 'config', '--local', 'user.name', GIT_USERNAME], capture_output=True, text=True, cwd=gitCwd)
    subprocess.run(
        ['git', 'config', '--local', 'user.email', GIT_EMAIL], capture_output=True, text=True, cwd=gitCwd)

    result = subprocess.run(
        ['git', 'add', '.'], capture_output=True, text=True, cwd=gitCwd)
    print(result.stderr)
    print(result.stdout)
    
    result = subprocess.run(
        ['git', 'commit', '-m', commitMsg], capture_output=True, text=True, cwd=gitCwd)
    print(result.stdout)
    print(result.stderr)

    gitUrl = genCloneUrl(gitPath)
    print(f"pushCode start {gitUrl} {fatureBranch} {gitPath} {wsPath}")
    result = subprocess.run(
        ['git', 'push', 'origin', fatureBranch], capture_output=True, text=True, cwd=gitCwd)
    if result.returncode != 0:
        print(result.stderr)
        return False, "git push failed:"+result.stderr

    print(f"push code success. in {wsPath}")
    return True, f"push code success. in {wsPath}"
    
def genCloneUrl(gitPath):
    # Extract the domain from the giturl
    domain = GIT_URL.split("//")[1]
    prot = GIT_URL.split("//")[0]

    # Combine the components to form the final URL
    finalUrl = f"{prot}//{GIT_USERNAME}:{GIT_TOKEN}@{domain}/{gitPath}.git"

    return finalUrl
