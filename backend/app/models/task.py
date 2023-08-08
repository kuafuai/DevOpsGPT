import datetime
from config import GRADE


def getEmptyTaskInfo():
    taskInfo = {
        "app_id": "",
        "task_id": "",
        "source_branch": "",
        "feature_branch": "",
        "final_requirement": ""
    }
    return {"memory": {"task_info": taskInfo, "originalPrompt": "", "repoPath": "", "clarifyRequirement": ""}}


def getTaskInfo(username, appID, sourceBranch, featureBranch):
    taskID = username+'-'+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    taskInfo = {
        "app_id": appID,
        "task_id": taskID,
        "source_branch": sourceBranch,
        "feature_branch": featureBranch
    }

    return taskInfo, True