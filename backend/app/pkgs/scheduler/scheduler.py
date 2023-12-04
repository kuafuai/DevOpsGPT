from app.models.async_task import AsyncTask
from app.pkgs.knowledge.app_info import repo_analyzer
import json
from datetime import datetime, timedelta
import threading

def task(app):
    print("scanning task ... ", datetime.now(), threading.current_thread().name, flush=True)
    with app.app_context():
        # 查询 任务
        async_task = AsyncTask.get_analyzer_code_task_one(AsyncTask.Status_Init)

        if async_task:
            print("process task token : ", async_task.token, async_task.version, flush=True)

            content = json.loads(async_task.task_content)
            type = content['type']
            repo = content['repo']
            lock_task = AsyncTask.update_task_status_and_version(async_task.id, AsyncTask.Status_Running, async_task.version)
            if lock_task:

                print("process lock task success token: ", async_task.token, async_task.version, lock_task.version)

                # 查询7天内的第一条成功记录，如果有直接更新结果
                history_success_data = AsyncTask.get_analyzer_code_by_name(async_task.task_name)
                if history_success_data:
                    print("find history :", history_success_data.token)
                    task_status_message = history_success_data.task_status_message
                    task_name = async_task.task_name+"(history)"
                    AsyncTask.update_task_status_and_message_and_name(async_task.id, AsyncTask.Status_Done, task_status_message, task_name)
                else:
                    try:
                        result, success = repo_analyzer(type, repo, async_task.id)
                        if success:
                            AsyncTask.update_task_status_and_message(async_task.id, AsyncTask.Status_Done, json.dumps(result))
                        else:
                            AsyncTask.update_task_status_and_message(async_task.id, AsyncTask.Status_Fail, result)
                    except Exception as e:
                        AsyncTask.update_task_status_and_message(async_task.id, AsyncTask.Status_Fail, "analyzer error")

            else:
                print("process lock task fail token: ", async_task.token)


def process_task_time_out(app):
    with app.app_context():
        async_task = AsyncTask.get_analyzer_code_task_one(AsyncTask.Status_Running)
        if async_task:
            current_date_1_hours = datetime.now() - timedelta(minutes=30)
            if current_date_1_hours > async_task.created_at:
                print("analyzer code timeout:", async_task.token)
                AsyncTask.update_task_status_and_message(async_task.id, AsyncTask.Status_Fail, "analyzer process timeout")