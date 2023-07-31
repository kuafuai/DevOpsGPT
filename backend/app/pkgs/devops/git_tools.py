import subprocess

import gitlab
from config import GITLAB_TOKEN, GITLAB_URL
from config import GITLAB_CLONE_URL
from config import WORKSPACE_PATH

# todo use git protocol with http(s)
def pullCode(ws_path, repo_path, base_branch, feature_branch):    
    result = subprocess.run(
        ['mkdir', '-p', ws_path], capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr)
        return False

    result = subprocess.run(['git', 'clone', '-b', base_branch, GITLAB_CLONE_URL+repo_path+'.git', repo_path], capture_output=True, text=True, cwd=ws_path)
    if result.returncode != 0:
        print(result.stderr)
        return False

    result = subprocess.run(
        ['git', 'checkout', '-b', feature_branch], capture_output=True, text=True, cwd=ws_path+'/'+repo_path)
    if result.returncode != 0:
        print(result.stderr)
        return False

    print("Code clone success.")
    return True

def createBranch(source_branch, branch_name, repopath):
    try:
        gl = gitlab.Gitlab(GITLAB_URL, GITLAB_TOKEN, api_version='4')

        project = gl.projects.get(repopath)

        branch = project.branches.get(branch_name)

        return "Branch already exists: %s" % branch_name
    except gitlab.GitlabGetError:
        try:
            branch = project.branches.create(
                {'branch': branch_name, 'ref': source_branch})
            return "Create branch successfully %s" % branch_name
        except Exception as e:
            return "Failed to create branch:" + str(e)
    except Exception as e:
        return "Failed to create branch" + str(e)
    
def pushCode(file_path, branch_name, repopath, content, commit_msg):
    try:
        print("get_file_content-repopath:" + repopath)
        print("get_file_content-branch_name:" + branch_name)
        print("get_file_content-file_path:" + file_path)
        gl = gitlab.Gitlab(GITLAB_URL, GITLAB_TOKEN, api_version='4')

        project = gl.projects.get(repopath)

        file = project.files.get(file_path, ref=branch_name)

        file.content = content
        file.save(branch_name, commit_msg)

        return GITLAB_URL + "/%s/-/blob/%s/%s" % (repopath, branch_name, file_path), True
    except gitlab.GitlabGetError:
        try:
            file = project.files.create({
                'file_path': file_path,
                'branch': branch_name,
                'content': content,
                'commit_message': commit_msg
            })
            return GITLAB_URL + "/%s/-/blob/%s/%s" % (repopath, branch_name, file_path), True
        except Exception as e:
            return "Failed to create file:" + str(e)
    except Exception as e:
        return "Failed to update file:" + str(e), False