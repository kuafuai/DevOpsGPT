import json

from flask import session
from app.pkgs.tools.i18b import getI18n
from app.pkgs.tools.i18b import getCurrentLanguageName
from app.pkgs.knowledge.app_info import getServiceStruct
from app.pkgs.tools.utils_tool import fix_llm_json_str
from app.pkgs.prompt.requirement_interface import RequirementInterface
from app.pkgs.tools.llm import chatCompletion

class RequirementBasic(RequirementInterface):
    def clarifyRequirement(self, userPrompt, globalContext):
        _ = getI18n("prompt") 
        requirementsDetail = _("Prerequisites, Detailed Operation Steps, Expected Results, Other Explanatory Notes.")

        username = session['username']
        apiDocUrl = session[username]['memory']['appconfig']['apiDocUrl']
        appStruct, _ = getServiceStruct(apiDocUrl)
    
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

Application Information：
```
"""+appStruct+"""
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

            message, success = chatCompletion(finalContext)
            
            if message.find("Nothing more to clarify") != -1 or message.find('"question":""') != -1 :
                return organize(firstPrompt, requirementsDetail)
        else:
            return organize(firstPrompt, requirementsDetail)

        
        return json.loads(message), success
    
def organize(firstPrompt, requirementsDetail):
    username = session['username']
    apiDocUrl = session[username]['memory']['appconfig']['apiDocUrl']
    appStruct, _ = getServiceStruct(apiDocUrl)
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

You need to base on "Application info" to analyze which services need to be modified to meet the requirements document you organize.
Application info：
```
"""+appStruct+"""
```

You should only directly respond in JSON format as described below, Ensure the response must can be parsed by Python json.loads, Response Format example:
{
"development_requirements_overview": "{The user's initial incoming development requirements}",
"development_requirements_detail": "{"""+requirementsDetail+"""}",
"service_modification_item": [{
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

    message, success = chatCompletion(Organize)
    message = fix_llm_json_str(message)
    return json.loads(message), success