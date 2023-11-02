from .scheduler import task


def register_job(scheduler, app):
    scheduler.add_job(task, 'interval', seconds=5, id="async_task", args=[app])
