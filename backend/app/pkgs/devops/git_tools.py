import os
import subprocess

def pullCode(ws_path, repo_path, base_branch, feature_branch, gitConfigList):
    gitConfig = gitConfigList[0]
    try:
        os.makedirs(ws_path, exist_ok=True)
    except Exception as e:
        return False, "mkdir failed: "+str(e)

    gitUrl = genCloneUrl(repo_path, gitConfig["git_url"], gitConfig["git_username"], gitConfig["git_token"])
    print(f"pullCode start {gitUrl} {base_branch} {repo_path} {ws_path}")
    # 先从feature_branch拉代码，如果失败再从base_branch拉
    try:
        result = subprocess.run(['git', 'clone', '-b', feature_branch, gitUrl, repo_path], capture_output=True, text=True, cwd=ws_path)
        if result.returncode != 0:
            print(result.stderr)
            return False, "git clone feature_branch failed: "+result.stderr
    except Exception as e:
        result = subprocess.run(['git', 'clone', '-b', base_branch, gitUrl, repo_path], capture_output=True, text=True, cwd=ws_path)
        if result.returncode != 0:
            print(result.stderr)
            return False, "git clone base_branch failed: "+result.stderr

        result = subprocess.run(
            ['git', 'checkout', '-b', feature_branch], capture_output=True, text=True, cwd=ws_path+'/'+repo_path)
        if result.returncode != 0:
            print(result.stderr)
            return False, "git checkout branch failed: "+result.stderr
    
    result = subprocess.run(
        ['git', 'config', 'pull.rebase', 'false'], capture_output=True, text=True, cwd=ws_path+'/'+repo_path)
    if result.returncode != 0:
        print(result.stderr)
        return False, "git config pull.rebase false failed: "+result.stderr

    print(f"Code clone success. in {ws_path}")
    return True, f"Code clone success. in {ws_path}"
    
def pushCode(wsPath, gitPath, fatureBranch, commitMsg, gitConfigList):
    gitConfig = gitConfigList[0]
    gitCwd = wsPath+'/'+gitPath

    try:
        os.makedirs(gitCwd, exist_ok=True)
    except Exception as e:
        return False, "mkdir failed: "+str(e)

    subprocess.run(
        ['git', 'config', '--local', 'user.name', gitConfig["git_username"]], capture_output=True, text=True, cwd=gitCwd)
    subprocess.run(
        ['git', 'config', '--local', 'user.email', gitConfig["git_email"]], capture_output=True, text=True, cwd=gitCwd)

    result = subprocess.run(
        ['git', 'add', '.'], capture_output=True, text=True, cwd=gitCwd)
    print(result.stderr)
    print(result.stdout)
    
    result = subprocess.run(
        ['git', 'commit', '-m', commitMsg], capture_output=True, text=True, cwd=gitCwd)
    print(result.stdout)
    print(result.stderr)

    gitUrl = genCloneUrl(gitPath, gitConfig["git_url"], gitConfig["git_username"], gitConfig["git_token"])
    print(f"pushCode start {gitUrl} {fatureBranch} {gitPath} {wsPath}")
    result = subprocess.run(
        ['git', 'push', 'origin', fatureBranch], capture_output=True, text=True, cwd=gitCwd)
    if result.returncode != 0:
        print(result.stderr)
        return False, "git push failed:"+result.stderr

    print(f"push code success. in {wsPath}")
    return True, f"push code success. in {wsPath}"
    
def genCloneUrl(gitPath, gitUrl, username, token):
    # Extract the domain from the giturl
    domain = gitUrl.split("//")[1]
    prot = gitUrl.split("//")[0]

    # Combine the components to form the final URL
    finalUrl = f"{prot}//{username}:{token}@{domain}/{gitPath}.git"

    return finalUrl

def gitResetWorkspace(wsPath, gitPath, fatureBranch, commitMsg, gitConfigList):
    gitConfig = gitConfigList[0]
    gitCwd = wsPath+'/'+gitPath

    try:
        os.makedirs(gitCwd, exist_ok=True)
    except Exception as e:
        return False, "mkdir failed: "+str(e)

    result = subprocess.run(
        ['git', 'fetch', 'origin', fatureBranch], capture_output=True, text=True, cwd=gitCwd)
    if result.returncode != 0:
        print(result.stderr)
        return False, "git fetch origin fatureBranch false failed: "+result.stderr
    
    result = subprocess.run(
        ['git', 'reset', '--hard', 'origin/'+fatureBranch], capture_output=True, text=True, cwd=gitCwd)
    if result.returncode != 0:
        print(result.stderr)
        return False, "git reset --hard origin fatureBranch false failed: "+result.stderr

    print(f"reset code success. in {wsPath}")
    return True, f"reset code success. in {wsPath}"
