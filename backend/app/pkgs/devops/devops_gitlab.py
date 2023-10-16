import gitlab
import html
import re
from app.pkgs.devops.devops_interface import DevopsInterface

class DevopsGitlab(DevopsInterface):
    def triggerPipeline(self, branch_name, serviceInfo, ciConfig):
        repopath = serviceInfo["git_path"]
        apiUrl = ciConfig["ci_api_url"]
        try:
            gl = gitlab.Gitlab(apiUrl, ciConfig["git_token"], api_version='4')

            project = gl.projects.get(repopath)
            pipeline = project.pipelines.create({'ref': branch_name})
            pipeline_url = apiUrl + '/' + repopath + '/-/pipelines/' + str(pipeline.id)
            return "Get pipline status...", str(pipeline.get_id()), pipeline_url, True
        except Exception as e:
            return f"Failed to trigger pipline giturl:{apiUrl} repopath:{repopath} branch:{branch_name}, Error:" + str(e), 0, "", False


    def getPipelineStatus(self, pipline_id, repopath, ciConfig):
        apiURL = ciConfig["ci_api_url"]
        try:
            gl = gitlab.Gitlab(apiURL, ciConfig["ci_token"], api_version='4')

            project = gl.projects.get(repopath)

            pipeline = project.pipelines.get(pipline_id)

            print("pipeline:", pipeline.status)

            jobs = pipeline.jobs.list()

            job_info = []
            docker_image = ""
            for job in jobs:
                print("job:", job)
                job_log = self.getPipelineJobLogs(repopath, pipline_id, job.id)
                job_info.append({
                    'job_id': job.id,
                    'job_name': job.name,
                    'status': job.status,
                    'duration': job.duration,
                    'log': job_log
                })
                img = parseDockerImage(job_log)
                if len(img) > 1:
                    docker_image = img

            return list(reversed(job_info)), docker_image, True
        except Exception as e:
            return "Failed to get pipline status:" + str(e), '', False

    def getPipelineJobLogs(self, repopath, pipeline_id, job_id, ciConfig):
        try:
            gl = gitlab.Gitlab(ciConfig["ci_api_url"], ciConfig["ci_token"], api_version='4')

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

def parseDockerImage(input_str):
    # 定义正则表达式模式
    pattern = r'kuafuai_docker_image_pushed:(.+?)[&|\n]'

    # 使用 re.search 来查找匹配项
    match = re.search(pattern, input_str)

    # 如果找到匹配项，则提取结果
    if match:
        result = match.group(1)
        return result
    else:
        print("parseDockerImage: 未找到匹配项")
        return ""