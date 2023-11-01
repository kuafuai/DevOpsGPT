from app.extensions import db


class AsyncTaskRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, nullable=False)
    step_idx = db.Column(db.Integer, nullable=False)

    task_record_title = db.Column(db.String(200))
    task_record_content = db.Column(db.String(200))

    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    @staticmethod
    def create_record(task_id, step_idx, task_record_title, task_record_content):
        st = AsyncTaskRecord(task_id=task_id, step_idx=step_idx, task_record_title=task_record_title,
                             task_record_content=task_record_content)
        db.session.add(st)
        db.session.commit()
        return st

    @staticmethod
    def get_record_by_task_id_and_step(task_id, step_idx):
        records = AsyncTaskRecord.query.filter_by(task_id=task_id, step_idx=step_idx).order_by(AsyncTaskRecord.id.desc()).limit(1).all()
        if len(records) == 1:
            return records[0]
        else:
            return None
