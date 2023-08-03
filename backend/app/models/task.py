import datetime
from config import DEMO_TASK_ID
from config import GRADE


def getEmptyTaskInfo():
    taskInfo = {
        "app_id": "",
        "task_id": "",
        "source_branch": "",
        "feature_branch": ""
    }
    return {"memory": {"task_info": taskInfo, "originalPrompt": "", "repoPath": "", "clarifyRequirement": ""}}


def getTaskInfo(username, appID, sourceBranch, featureBranch):
    if GRADE == "base":
        taskID = DEMO_TASK_ID
    else:
        taskID = username+'-'+datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    taskInfo = {
        "app_id": appID,
        "task_id": taskID,
        "source_branch": sourceBranch,
        "feature_branch": featureBranch
    }

    return taskInfo, True