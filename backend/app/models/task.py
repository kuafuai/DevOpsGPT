import datetime
from config import GRADE


def getEmptyTaskInfo():
    taskInfo = {
        "app_id": "",
        "task_id": "",
        "source_branch": "",
        "feature_branch": "",
        "final_requirement": "",
        "organize": ""
    }
    return {"memory": {"task_info": taskInfo, "originalPrompt": "", "repoPath": "", "clarifyRequirement": ""}}
