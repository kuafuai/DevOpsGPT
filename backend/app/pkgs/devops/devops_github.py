import html
import time
import requests
import re
from app.pkgs.devops.devops_interface import DevopsInterface

class DevopsGitHub(DevopsInterface):
    def triggerPipeline(self, branch_name, serviceInfo, ciConfig):
        print(ciConfig)

        ciURL = ciConfig["ci_api_url"]
        ciToken = ciConfig["ci_token"]
        repopath = serviceInfo["git_path"]
        gitWorkflow = serviceInfo["git_workflow"]
        try:
            pipeline_url = f"{ciURL}/repos/{repopath}/actions/workflows/{gitWorkflow}/dispatches"
            headers = {
                "Authorization": f"Bearer {ciToken}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28"
            }
            data = {
                "ref": branch_name
            }
            print(pipeline_url, flush=True)
            response = requests.post(pipeline_url, json=data, headers=headers)
            print(response, flush=True)

            if response.status_code == 204:
                print("Pipeline triggered successfully.")
                time.sleep(3)

                # Get the most recent record
                workflow_url = f"{ciURL}/repos/{repopath}/actions/workflows/{gitWorkflow}/runs"
                response = requests.get(workflow_url, headers=headers)
                #print(response.json())
                if response.status_code == 200:
                    runs = response.json()["workflow_runs"]
                    for run in runs:
                        run_id = run["id"]
                        break

                return "Get pipline status...", run_id, f"https://github.com/{repopath}/actions/runs/{run_id}", True
            else:
                return f"Failed to trigger pipeline 【Please confirm that the code has been pushed】. giturl:{ciURL} repopath:{repopath} branch:{branch_name} gitWorkflow:{gitWorkflow}, Error: {str(e)}", 0, "", False
        except Exception as e:
            return f"Failed to trigger pipeline 【Please confirm that the code has been pushed】. giturl:{ciURL} repopath:{repopath} branch:{branch_name} gitWorkflow:{gitWorkflow}, Error: {str(e)}", 0, "", False

    def getPipelineStatus(self, run_id, repopath, ciConfig):
        ciToken = ciConfig["ci_token"]
        ciURL = ciConfig["ci_api_url"]
        try:
            headers = {
                "Authorization": f"Bearer {ciToken}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28"
            }
            
            run_details_url = f"{ciURL}/repos/{repopath}/actions/runs/{run_id}"
            run_response = requests.get(run_details_url, headers=headers)
            print(run_response)
            
            if run_response.status_code == 200:
                print(run_response.json())
                job_log_url = run_response.json()["jobs_url"]

                run_details = requests.get(job_log_url, headers=headers)
                if run_details.status_code == 200:
                    # 获取阶段信息
                    jobs = run_details.json()["jobs"]
                    
                    job_info = []
                    docker_image = ""
                    for job in jobs:
                        print("job:", job)
                        if job["conclusion"] is None:
                                job["conclusion"] = "none"
                                job["completed_at"] = "none"
                                
                        steps = ""
                        for step in job["steps"]:
                            if step["conclusion"] is None:
                                step["conclusion"] = "none"
                            steps += step["name"]+"<br>"+step["conclusion"]+"<br><br>"
                        
                        job_log = self.getPipelineJobLogs(repopath, run_id, job["id"], ciConfig)
                        img = parseDockerImage(job_log)
                        if len(img) > 1:
                            docker_image = img

                        job_info.append({
                            'job_id': job["id"],
                            'job_name': job["name"],
                            'status': "none" if job["status"]=="in_progress" else ("failed" if job["conclusion"]=="failure" else job["conclusion"]),
                            'duration': "none" if job["status"]=="in_progress" else job["completed_at"],
                            'log': steps + "<br><br>" + job_log
                        })

                    return list(reversed(job_info)), docker_image, True
            return f"Failed to get pipeline status for repo {repopath} and pipeline ID {run_id}, Error: {str(e)}", '', False
        except Exception as e:
            return f"Failed to get pipeline status for repo {repopath} and pipeline ID {run_id}, Error: {str(e)}", '', False

    def getPipelineJobLogs(self, repopath, pipeline_id, job_id, ciConfig):
        ciToken = ciConfig["ci_token"]
        try:
            headers = {
                "Authorization": f"Bearer {ciToken}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28"
            }

            url = f"https://api.github.com/repos/{repopath}/actions/jobs/{job_id}/logs"
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                logs = response.text
                return removeColorCodes(logs)
            else:
                return f"Failed to get log for job {job_id} in repo {repopath}. Status code: {response.status_code}"
        except Exception as e:
            return f"Failed to get log for job {job_id} in repo {repopath}, Error: {str(e)}"

def removeColorCodes(log_string):
    color_regex = re.compile(r'\x1b\[[0-9;]*m')
    cleaned_string = re.sub(color_regex, '', log_string)
    cleaned_string = re.sub(r'\n', '<br>', cleaned_string)
    cleaned_string = re.sub(r'\r', '<br>', cleaned_string)
    cleaned_string = re.sub('"', ' ', cleaned_string)
    cleaned_string = re.sub("'", ' ', cleaned_string)
    cleaned_string = re.sub(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]', ' ', cleaned_string)
    cleaned_string = html.escape(cleaned_string)
    return cleaned_string

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