from app.extensions import db
import time
import hashlib
from datetime import datetime


class AsyncTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(50))
    task_type = db.Column(db.Integer, nullable=False)
    task_name = db.Column(db.String(100))
    task_content = db.Column(db.String(200))
    task_status = db.Column(db.Integer, nullable=False)
    task_status_message = db.Column(db.String(200))
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    Status_Init = 0
    Status_Running = 1
    Status_Done = 2
    Status_Fail = 3

    Type_Analyzer_Code = 1

    @staticmethod
    def create_task(task_type, task_name, task_content):
        hash_object = hashlib.md5()
        hash_object.update(str(time.time()).encode('utf-8'))
        md5_hash = hash_object.hexdigest()

        st = AsyncTask(token=md5_hash, task_type=task_type, task_name=task_name, task_content=task_content,
                       task_status=AsyncTask.Status_Init, task_status_message="Init Task")

        db.session.add(st)
        db.session.commit()
        return st

    @staticmethod
    def get_task_by_token(token):
        st = AsyncTask.query.filter_by(token=token).one()

        return st

    @staticmethod
    def get_analyzer_code_task_one():
        query_tasks = AsyncTask.query.filter(AsyncTask.task_type == AsyncTask.Type_Analyzer_Code,
                                             AsyncTask.task_status.in_(
                                                 [AsyncTask.Status_Init, AsyncTask.Status_Running])
                                             ).limit(1).all()
        if len(query_tasks) == 1:
            return query_tasks[0]
        else:
            return None

    @staticmethod
    def update_task_status(task_id, status):
        task = AsyncTask.query.get(task_id)
        if task:
            task.updated_at = datetime.utcnow()
            task.task_status = status
            db.session.commit()

            return task
        else:
            return None

    @staticmethod
    def update_task_message(task_id, message):
        task = AsyncTask.query.get(task_id)
        if task:
            task.updated_at = datetime.utcnow()
            task.task_status_message = message
            db.session.commit()

            return task
        else:
            return None

    @staticmethod
    def update_task_status_and_message(task_id, status, message):
        task = AsyncTask.query.get(task_id)
        if task:
            task.updated_at = datetime.utcnow()
            task.task_status = status
            task.task_status_message = message
            db.session.commit()

            return task
        else:
            return None
