import json
from flask import session
from app.pkgs.tools.i18b import getI18n
from app.pkgs.tools.i18b import getCurrentLanguageName
from app.pkgs.tools.utils_tool import fix_llm_json_str
from app.pkgs.prompt.requirement_interface import RequirementInterface
from app.pkgs.tools.llm import chatCompletion
from app.pkgs.knowledge.app_info import getAppArchitecture

class RequirementBasic(RequirementInterface):
    def clarifyRequirement(self, userPrompt, globalContext, appArchitecture):
        _ = getI18n("prompt") 
        requirementsDetail = _("Prerequisites, Detailed Operation Steps, Expected Results, Other Explanatory Notes.")
    
        firstPrompt = ""
        preContext = []
        try:
            preContext = json.loads(globalContext)
        except Exception as e:
            print(str(e))

        maxCycle = 2
        message = ""
        if len(preContext) == 0:
            session[session["username"]]["memory"]["clarifyRequirement"] = ""
            firstPrompt = userPrompt
        elif len(preContext) < maxCycle:
            firstPrompt = preContext[0]["content"]
            session[session["username"]]["memory"]["clarifyRequirement"] += userPrompt + "\n"
            
            preContext = preContext[1:]
            preContext.append({
                "role": "user",
                "content": userPrompt + """

Is there anything else unclear? If yes, continue asking less than 3 unclear questions in the same format as before, If no, only directly respond \"Nothing more to clarify.\"
"""
            })
        else:
            firstPrompt = preContext[0]["content"]
            session[session["username"]]["memory"]["clarifyRequirement"] += userPrompt

        if len(preContext) < maxCycle:
            finalContext = [
                {
                "role": "system",
                "content": """As a senior full stack developer. Your task is to read user software development requirement and clarify or confirm them to complete a requirement document that integrates the requirement into the application. The document should include """+requirementsDetail+""".

Specifically, First you need to think about a simple step-by-step guide, then provide a list of less than 5 highly relevant questions to clarify or confirm, and then wait for the user's answers. 
As a senior programmer, you have a lot of expertise based on which to guide users to clarify requirements, don't ask stupid questions.

Application Information:
```
"""+appArchitecture+"""
```

Software development requirement:
```
"""+firstPrompt+"""
```

You should only directly respond in JSON format as described below, Ensure the response must can be parsed by Python json.loads, Response Format example:
[{"question":"question","reasoning":"reasoning","answer_sample":"Answer sample"},{"question":"question","reasoning":"reasoning","answer_sample":"Answer sample"}]
Follow the JSON response exactly as above.

Note: Keep conversations in """+getCurrentLanguageName()+""".
"""
                }
            ]
            finalContext.extend(preContext)

            message, success = chatCompletion(finalContext, FAKE_CLARIFY_1)
            
            if message.find("Nothing more to clarify") != -1 or message.find('"question":""') != -1 :
                return organize(firstPrompt, requirementsDetail)
        else:
            return organize(firstPrompt, requirementsDetail, appArchitecture)

        message = fix_llm_json_str(message)
        return json.loads(message), success
    
def organize(firstPrompt, requirementsDetail, appArchitecture):
    Organize = []
    Organize.append({
        "role": "system",
        "content": """
As a senior software developer, you will organize a long and detailed requirement document include """+requirementsDetail+""" based on the "software development requirement" and "clarified list".
Think step by step make sure the "clarified list" answers are all taken into account, do not miss any details.
The answers from the 'clarified list' are of utmost importance and must be included in the requirement document with as much detail as possible.

software development requirement:
```
"""+firstPrompt+"""
```

clarified list:
```
"""+session[session["username"]]["memory"]["clarifyRequirement"]+"""
```

You need to base on "Application Information" to analyze which services need to be modified to meet the requirements document you organize.
Application Information:
```
"""+appArchitecture+"""
```

You should only directly respond in JSON format as described below, Ensure the response must can be parsed by Python json.loads, Response Format example:
{
"development_requirements_overview": "{The user's initial incoming development requirements}",
"development_requirements_detail": "{"""+requirementsDetail+"""}",
"services_involved": [{
    "service-name": "xxx1",
    "reasoning": "reasoning"
}, {
    "service-name": "xxx2",
    "reasoning": "reasoning"
}]
}

Note: Keep conversations in """+getCurrentLanguageName()+""".
"""
    })

    message, success = chatCompletion(Organize, FAKE_CLARIFY_2)
    print("------")
    print(message)
    message = fix_llm_json_str(message)
    return json.loads(message), success

FAKE_CLARIFY_1 = """
    [
        {
            "question": "这个贪吃蛇游戏需要有什么样的界面和图形效果吗？",
            "reasoning": "界面和图形效果是游戏的重要组成部分，需要确认用户对界面和图形效果的要求。",
            "answer_sample": "需要一个简单的游戏界面，贪吃蛇和食物应该有明显的图形表示。"
        },
        {
            "question": "贪吃蛇的移动速度是固定的还是可以调整的？",
            "reasoning": "移动速度是游戏的一个重要参数，需要确认用户对贪吃蛇移动速度的要求。",
            "answer_sample": "贪吃蛇的移动速度应该是可调整的，用户可以根据自己的喜好来设置速度。"
        },
        {
            "question": "贪吃蛇吃到食物后会变长吗？",
            "reasoning": "贪吃蛇吃到食物后是否会变长是游戏规则的一部分，需要确认用户对此的要求。",
            "answer_sample": "是的，贪吃蛇吃到食物后应该会变长一节。"
        }
    ]
"""

FAKE_CLARIFY_2 = """
    {
        "development_requirements_overview": "开发一个经典的贪吃蛇的网页小游戏，通过键盘控制贪吃蛇的上下左右移动",
        "development_requirements_detail": "前置条件：无<br><br>详细操作步骤：<br>1. 打开游戏界面<br>2. 使用键盘上下左右箭头键控制贪吃蛇的移动<br>3. 贪吃蛇吃到食物后会变长一节<br>4. 游戏结束条件：贪吃蛇撞到墙壁或撞到自己的身体<br><br>预期结果：<br>- 游戏界面显示贪吃蛇和食物的图形表示<br>- 贪吃蛇根据用户的键盘操作进行移动<br>- 贪吃蛇吃到食物后会变长一节<br>- 游戏结束时显示游戏结束的提示信息<br><br>其他解释说明：<br>- 贪吃蛇的移动速度应该是可调整的，用户可以根据自己的喜好来设置速度",
        "services_involved": [{
            "service-name": "free_demo",
            "reasoning": "The free_demo service can be used to develop the requirements for the snake game as it is a general-purpose service that can be used for any requirements."
        }]
    }
"""