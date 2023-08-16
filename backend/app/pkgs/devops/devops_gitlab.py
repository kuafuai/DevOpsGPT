import gitlab
import html
import re
from app.pkgs.devops.devops_interface import DevopsInterface
from config import GIT_TOKEN, GIT_URL

class DevopsGitlab(DevopsInterface):
    def triggerPipeline(self, branch_name, repopath, gitWorkflow):
        try:
            gl = gitlab.Gitlab(GIT_URL, GIT_TOKEN, api_version='4')

            project = gl.projects.get(repopath)
            pipeline = project.pipelines.create({'ref': branch_name})
            pipeline_url = GIT_URL + '/' + repopath + '/-/pipelines/' + str(pipeline.id)
            return "Get pipline status...", str(pipeline.get_id()), pipeline_url, True
        except Exception as e:
            return f"Failed to trigger pipline giturl:{GIT_URL} repopath:{repopath} branch:{branch_name}, Error:" + str(e), 0, "", False


    def getPipelineStatus(self, pipline_id, repopath):
        try:
            gl = gitlab.Gitlab(GIT_URL, GIT_TOKEN, api_version='4')

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
                    'log': self.getPipelineJobLogs(repopath, pipline_id, job.id)
                })

            return list(reversed(job_info)), True
        except Exception as e:
            return "Failed to get pipline status:" + str(e), False

    def getPipelineJobLogs(self, repopath, pipeline_id, job_id):
        try:
            gl = gitlab.Gitlab(GIT_URL, GIT_TOKEN, api_version='4')

            project = gl.projects.get(repopath)
            job = project.jobs.get(job_id)
            logs = job.trace()

            return removeColorCodes(logs)
        except Exception as e:
            return "Failed to get log: " + str(e)


def removeColorCodes(log_string):
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

    # def getFileContent(self, file_path, branch_name, repopath):
    #     try:
    #         print("get_file_content-repopath:" + repopath)
    #         print("get_file_content-branch_name:" + branch_name)
    #         print("get_file_content-file_path:" + file_path)
    #         gl = gitlab.Gitlab(GIT_URL, private_token=GIT_TOKEN, api_version='4')

    #         project = gl.projects.get(repopath)

    #         file = project.files.get(file_path, ref=branch_name)

    #         content = codecs.decode(file.decode(), 'utf-8')

    #         print(content)

    #         return True, content
    #     except Exception as e:
    #         return False, str(e)
