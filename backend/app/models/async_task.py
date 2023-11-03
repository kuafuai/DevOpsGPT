from app.extensions import db
import time
import hashlib
from datetime import datetime, timedelta


class AsyncTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(50))
    task_type = db.Column(db.Integer, nullable=False)
    task_name = db.Column(db.String(100))
    task_content = db.Column(db.String(200))
    task_status = db.Column(db.Integer, nullable=False)
    task_status_message = db.Column(db.String(200))
    ip = db.Column(db.String(50))
    version = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    Status_Init = 0
    Status_Running = 1
    Status_Done = 2
    Status_Fail = 3

    Type_Analyzer_Code = 1

    Search_Process_Key = "process"
    Search_Done_key = "done"

    Search_Process_Value = [Status_Init, Status_Running]
    Search_Done_Value = [Status_Done, Status_Fail]
    Search_All_Value = [Status_Init, Status_Running, Status_Done, Status_Fail]

    @staticmethod
    def create_task(task_type, task_name, task_content, ip):
        hash_object = hashlib.md5()
        hash_object.update(str(time.time()).encode('utf-8'))
        md5_hash = hash_object.hexdigest()

        st = AsyncTask(token=md5_hash, task_type=task_type, task_name=task_name, task_content=task_content,
                       task_status=AsyncTask.Status_Init, task_status_message="Init Task", ip=ip, version=0,
                       created_at=datetime.now())

        db.session.add(st)
        db.session.commit()
        return st

    @staticmethod
    def get_task_by_token(token):
        st = AsyncTask.query.filter_by(token=token).first()

        return st

    @staticmethod
    def get_analyzer_code_task_one(status):
        query_tasks = AsyncTask.query.filter(AsyncTask.task_type == AsyncTask.Type_Analyzer_Code,
                                             AsyncTask.task_status.in_([status])
                                             ).limit(1).all()
        if len(query_tasks) == 1:
            return query_tasks[0]
        else:
            return None

    @staticmethod
    def get_analyzer_code_by_name(task_name):
        today = datetime.today()
        start_date = today - timedelta(days=7)

        query_tasks = AsyncTask.query.filter(AsyncTask.task_type == AsyncTask.Type_Analyzer_Code,
                                             AsyncTask.task_status.in_([AsyncTask.Status_Done]),
                                             AsyncTask.created_at >= start_date,
                                             AsyncTask.created_at <= today,
                                             AsyncTask.task_name == task_name).limit(1).all()
        if len(query_tasks) == 1:
            return query_tasks[0]
        else:
            return None

    # 今天 分析代码
    @staticmethod
    def get_today_analyzer_code_count(ip, type):
        if type == AsyncTask.Search_Process_Key:
            param_status = AsyncTask.Search_Process_Value
        elif type == AsyncTask.Search_Done_key:
            param_status = AsyncTask.Search_Done_Value
        else:
            param_status = AsyncTask.Search_All_Value

        today = datetime.today()
        start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)

        count = AsyncTask.query.filter(AsyncTask.task_type == AsyncTask.Type_Analyzer_Code,
                                       AsyncTask.task_status.in_(param_status),
                                       AsyncTask.created_at >= start_date,
                                       AsyncTask.created_at <= today,
                                       AsyncTask.ip == ip).count()
        return count

    @staticmethod
    def get_today_analyzer_code_list(ip, type):
        if type == AsyncTask.Search_Process_Key:
            param_status = AsyncTask.Search_Process_Value
        elif type == AsyncTask.Search_Done_key:
            param_status = AsyncTask.Search_Done_Value
        else:
            param_status = AsyncTask.Search_All_Value

        today = datetime.today()
        start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)

        query_tasks = AsyncTask.query.filter(AsyncTask.task_type == AsyncTask.Type_Analyzer_Code,
                                             AsyncTask.task_status.in_(param_status),
                                             AsyncTask.created_at >= start_date,
                                             AsyncTask.created_at <= today,
                                             AsyncTask.ip == ip).limit(1).all()
        if len(query_tasks) == 1:
            return query_tasks[0]
        else:
            return None

    @staticmethod
    def update_task_status(task_id, status):
        task = AsyncTask.query.get(task_id)
        if task:
            task.updated_at = datetime.now()
            task.task_status = status
            db.session.commit()

            return task
        else:
            return None

    @staticmethod
    def update_task_status_and_version(task_id, status, version):
        task = AsyncTask.query.get(task_id)
        if task and task.version == version:

            task.updated_at = datetime.now()
            task.task_status = status
            task.version = task.version + 1
            db.session.commit()

            return task
        else:
            return None

    @staticmethod
    def update_task_message(task_id, message):
        task = AsyncTask.query.get(task_id)
        if task:
            task.updated_at = datetime.now()
            task.task_status_message = message
            db.session.commit()

            return task
        else:
            return None

    @staticmethod
    def update_task_status_and_message(task_id, status, message):
        task = AsyncTask.query.get(task_id)
        if task:
            task.updated_at = datetime.now()
            task.task_status = status
            task.task_status_message = message
            db.session.commit()

            return task
        else:
            return None

    @staticmethod
    def update_task_status_and_message_and_name(task_id, status, message, name):
        task = AsyncTask.query.get(task_id)
        if task:
            task.updated_at = datetime.now()
            task.task_status = status
            task.task_status_message = message
            task.task_name = name
            db.session.commit()

            return task
        else:
            return None
