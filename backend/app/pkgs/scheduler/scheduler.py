from app.models.async_task import AsyncTask
from app.pkgs.knowledge.app_info import repo_analyzer
import json


def task(app):
    print("scanning task ... ")
    with app.app_context():
        async_task = AsyncTask.get_analyzer_code_task_one()

        if async_task:
            print("process task token : ", async_task.token)

            content = json.loads(async_task.task_content)
            type = content['type']
            repo = content['repo']
            AsyncTask.update_task_status(async_task.id, AsyncTask.Status_Running)
            result, success = repo_analyzer(type, repo, async_task.id)
            if success:
                AsyncTask.update_task_status_and_message(async_task.id, AsyncTask.Status_Done, json.dumps(result))
            else:
                AsyncTask.update_task_status_and_message(async_task.id, AsyncTask.Status_Fail, "分析失败")
