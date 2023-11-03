from .scheduler import task, process_task_time_out


def register_job(scheduler, app):
    scheduler.add_job(task, 'interval', seconds=5, id="async_task", args=[app], max_instances=5)
    scheduler.add_job(process_task_time_out, 'interval', seconds=10, id="async_task_time_out", args=[app])
