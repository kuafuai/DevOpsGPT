import html
import json
import time
import requests
import re
from app.pkgs.devops.devops_interface import DevopsInterface
from config import GIT_TOKEN, GIT_API, GIT_URL

class DevopsGitHub(DevopsInterface):
    def triggerPipeline(self, branch_name, repopath, gitWorkflow):
        try:
            pipeline_url = f"{GIT_API}/repos/{repopath}/actions/workflows/{gitWorkflow}/dispatches"
            headers = {
                "Authorization": f"Bearer {GIT_TOKEN}",
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
                workflow_url = f"{GIT_API}/repos/{repopath}/actions/workflows/{gitWorkflow}/runs"
                response = requests.get(workflow_url, headers=headers)
                print(response.json())
                if response.status_code == 200:
                    runs = response.json()["workflow_runs"]
                    for run in runs:
                        run_id = run["id"]
                        break

                return "Get pipline status...", run_id, f"{GIT_URL}/{repopath}/actions/runs/{run_id}", True
            else:
                return f"Failed to trigger pipeline giturl:{GIT_API} repopath:{repopath} branch:{branch_name} gitWorkflow:{gitWorkflow}, Error: {str(e)}", 0, "", False
        except Exception as e:
            return f"Failed to trigger pipeline giturl:{GIT_API} repopath:{repopath} branch:{branch_name} gitWorkflow:{gitWorkflow}, Error: {str(e)}", 0, "", False

    def getPipelineStatus(self, run_id, repopath):
        try:
            headers = {
                "Authorization": f"Bearer {GIT_TOKEN}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28"
            }
            
            run_details_url = f"{GIT_API}/repos/{repopath}/actions/runs/{run_id}"
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
                        job_info.append({
                            'job_id': job["id"],
                            'job_name': job["name"],
                            'status': "none" if job["status"]=="in_progress" else ("failed" if job["conclusion"]=="failure" else job["conclusion"]),
                            'duration': "none" if job["status"]=="in_progress" else job["completed_at"],
                            'log': steps
                        })

                    return list(reversed(job_info)), True
            return f"Failed to get pipeline status for repo {repopath} and pipeline ID {run_id}, Error: {str(e)}", False
        except Exception as e:
            return f"Failed to get pipeline status for repo {repopath} and pipeline ID {run_id}, Error: {str(e)}", False

    def getPipelineJobLogs(self, repopath, pipeline_id, job_id):
        try:
            headers = {
                "Authorization": f"Bearer {GIT_TOKEN}",
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
