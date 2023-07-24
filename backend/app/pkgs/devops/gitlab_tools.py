import gitlab
import codecs
import html
import re
import subprocess

from config import GITLAB_TOKEN, GITLAB_URL, GITLAB_CLONE_URL


def get_file_content(file_path, branch_name, repopath):
    try:
        print("get_file_content-repopath:" + repopath)
        print("get_file_content-branch_name:" + branch_name)
        print("get_file_content-file_path:" + file_path)
        gl = gitlab.Gitlab(GITLAB_URL, private_token=GITLAB_TOKEN, api_version='4')

        project = gl.projects.get(repopath)

        file = project.files.get(file_path, ref=branch_name)

        content = codecs.decode(file.decode(), 'utf-8')

        print(content)

        return True, content
    except Exception as e:
        return False, str(e)


def update_file_content(file_path, branch_name, repopath, content, commit_msg):
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


def trigger_pipeline(branch_name, repopath):
    try:
        gl = gitlab.Gitlab(GITLAB_URL, GITLAB_TOKEN, api_version='4')

        project = gl.projects.get(repopath)
        pipeline = project.pipelines.create({'ref': branch_name})
        pipeline_url = GITLAB_URL + \
            repopath + '/-/pipelines/' + str(pipeline.id)
        return "Get pipline status...", str(pipeline.get_id()), pipeline_url, True
    except Exception as e:
        return "Failed to trigger pipline:" + str(e), 0, "", False


def get_pipeline_status(pipline_id, repopath):
    try:
        gl = gitlab.Gitlab(GITLAB_URL, GITLAB_TOKEN, api_version='4')

        project = gl.projects.get(repopath)

        pipeline = project.pipelines.get(pipline_id)

        print("pipeline:", pipeline.status)

        jobs = pipeline.jobs.list()

        job_info = []
        for job in jobs:
            print("job:", job)
            job_info.append({
                'job_id': job.id,
                'job_name': job.name,
                'status': job.status,
                'duration': job.duration,
                'log': get_pipeline_job_logs(repopath, pipline_id, job.id)
            })

        return list(reversed(job_info))
    except Exception as e:
        return "Failed to get pipline status:" + str(e)


def check_and_create_branch(source_branch, branch_name, repopath):
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


def get_pipeline_job_logs(repopath, pipeline_id, job_id):
    try:
        gl = gitlab.Gitlab(GITLAB_URL, GITLAB_TOKEN, api_version='4')

        project = gl.projects.get(repopath)
        job = project.jobs.get(job_id)
        logs = job.trace()

        return remove_color_codes(logs)
    except Exception as e:
        return "Failed to get log: " + str(e)


def remove_color_codes(log_string):
    unicode_string = log_string.decode('unicode_escape')
    color_regex = re.compile(r'\x1b\[[0-9;]*m')
    cleaned_string = re.sub(color_regex, '', unicode_string)
    cleaned_string = re.sub(r'\n', '<br>', unicode_string)
    cleaned_string = re.sub(r'\r', '<br>', cleaned_string)
    cleaned_string = re.sub('"', ' ', cleaned_string)
    cleaned_string = re.sub("'", ' ', cleaned_string)
    cleaned_string = re.sub(
        r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]', ' ', cleaned_string)
    cleaned_string = html.escape(cleaned_string)
    return cleaned_string


def pull_code(ws_path, repo_path, base_branch, feature_branch):    
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