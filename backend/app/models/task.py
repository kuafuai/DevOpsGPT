import datetime
from config import DEMO_TASK_ID
from config import GRADE


def getEmptyTaskInfo():
    return {"memory": {"appconfig": {"appName": ""}, "originalPrompt": "", "repoPath": "", "clarifyRequirement": ""}}


def getTaskInfo(username, appName, appID, appIntro, repoList, apiDocUrl, sourceBranch, featureBranch):
    if len(appName) > 0 and len(sourceBranch) and len(featureBranch):
        if GRADE == "base":
            taskID = DEMO_TASK_ID
        else:
            taskID = username+'-'+datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        appInfo = {
            "appName": appName,
            "appID": appID,
            "appIntro": appIntro,
            "repoList": repoList,
            "taskID": taskID,
            "apiDocUrl": apiDocUrl,
            "sourceBranch": sourceBranch,
            "featureBranch": featureBranch
        }

        return appInfo, True
    else:
        return "", False
