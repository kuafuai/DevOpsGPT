import json
import time
from app.pkgs.tools.llm import chatCompletion
from app.pkgs.tools.utils_tool import fix_llm_json_str
from app.pkgs.prompt.subtask_interface import SubtaskInterface
from app.pkgs.knowledge.app_info import getServiceSpecification, getServiceStruct
from config import MODE
from app.pkgs.tools.i18b import getCurrentLanguageName

class SubtaskBasic(SubtaskInterface):
    def splitTask(self, feature, serviceName, appBasePrompt, projectInfo, projectLib, serviceStruct, appID):
        if MODE == "FAKE":
            time.sleep(10)
            return TEST_RESULT, True

        data, success = setpReqChooseLib(feature, appBasePrompt, projectInfo, projectLib)
        code_require = []
        default_msg, _ = getServiceSpecification(appID, serviceName, "Default")
        code_require.append(default_msg)
        for t in data:
            name = t['name']
            require_msg, _ = getServiceSpecification(appID, serviceName, name)
            code_require.append(require_msg)

        code_require = list(set(code_require))
        print(f"get code_require:{code_require}")
        specification = '\n'.join(code_require)

        message, ctx, success = setp1Task(feature, appBasePrompt, serviceStruct, specification)
        if success:
            return setp2Code(message, feature, appBasePrompt, specification, serviceStruct)
        else:
            return message, False


def setp2Code(message, feature, appBasePrompt, specification, serviceStruct):
    context = []
    context.append({
        "role": "system",
        "content": """
As a senior full stack developer. 
You will get "Code directory structure" and "Development specification" and "Development requirement" and "Development steps" for code to write.  

Code directory structure:
```
""" + serviceStruct + """
```

Development specification:
""" + specification + """  

Development requirement:
```
""" + feature + """
````

Development steps
```
""" + message + """
```


According to the above information, you will write a very long answer. Make sure that requirements are properly and fully implemented in code.
Think step by step to make sure our code is complete and run correctly.
Don't be lazy, don't miss any code, all code should respond to the output.

Please note that the code should be fully functional. No placeholders no todo. Constantly rethinking whether the code is complete. Ensure correlation and integrity between different code files to ensure that all code works correctly.

Then you will output the content of each file including ALL code.
Each file must strictly follow a JSON code block format as below.
Please respond in """+getCurrentLanguageName()+"""".

Format example:
```
[
    {
      "file-path": "src/aaa.java",
      "reference-file": "",
      "code-interpreter": "",
      "code": ""
    },
    {
      "file-path": "main.go",
      "reference-file": "",
      "code-interpreter": "",
      "code": ""
    }
]
Do not explain, return JSON directly, Ensure the response can be parsed by Python json.loads.

JSON Field description:
```
1. "code-interpreter": As a senior developer, you first need to design the code and add detailed instructions. For example: lay out the names of the core classes, functions, methods that will be necessary, specific variable names and types to be added and modified, method names to be added or modified, parameter names, and so on. this field respond in """+getCurrentLanguageName()+"""".
2. "reference-file": Inference only based on the "Directory structure" "reference-file" filed above, if you don't know leave it blank.
```
        """
    })

    data, success = chatCompletion(context)
    
    data = fix_llm_json_str(data)

    if data.startswith('{') and data.endswith('}'):
        data = "[" + data + "]"

    return json.loads(data), success

def setp1Task(feature, appBasePrompt, serviceStruct, specification):
    context = []
    content = appBasePrompt + """. Your job is to think step by step according to the basic "Code directory structure" and "Development specification" provided below, and break down the "Development requirement" provided below into multiple steps from the perspective of completing code development. Each step needs to be detailed.
Be careful to analyze only the steps, do not write code, and decomposition should be appropriate and reasonable, neither over-splitting nor missing key steps.

Note that, these steps should not include anything that is not related to developing code, such as preparing the environment, performing tests, performing packaging, deploying, and so on.

Code directory structure:
```
""" + serviceStruct + """
```

Development specification:
```
""" + specification + """  
```

Development requirement:
```
""" + feature + """
````

Do not explain and talk, directly respond substeps.
"""
    context.append({"role": "system", "content": content})
    message, success = chatCompletion(context)

    return message, context, success


# choose lib by req
def setpReqChooseLib(feature, appBasePrompt, projectInfo, projectLib):
    context = []
    content = appBasePrompt + """, Your task is to analyze the requirements and find the appropriate component names. Think step by step, combine the existing project information and the existing component list, analyze the user input requirements to use which components, be careful to select only among the existing components. Please do not write code

Note that the returned component name must contain only the name but not the description. In addition, the component name must be exactly the same as that in the component list.

Service Information:
```
""" + projectInfo + """
```
    
components list:
```
""" + projectLib + """
```

requirements:
```
""" + feature + """
```
    """
    context.append({"role": "system", "content": content})
    message, success = chatCompletion(context)

    context.append({
        "role": "assistant",
        "content": message
    })

    context.append({
        "role": "user",
        "content": """Summary of the components chosen above.you will provide only the output in the exact format specified below with no explanation or conversation.

You should only directly respond in JSON format as described below, Ensure the response must can be parsed by Python json.loads, Response Format example:
```
[{"name":"{the name without a description}","reason":"reason","description":"description"}]
```
"""
    })

    data, success = chatCompletion(context)

    return json.loads(data), success

# just for test
TEST_RESULT = [{
    "service-name": "java_demo_backend",
    "files": [
        {
            "file-path": "src/main/resources/db/migration/V202307081234__create_member_table.sql",
            "reference-file": "src/main/resources/db/migration/V202301__create_target_table.sql",
            "code": "CREATE TABLE t_member (\n  id INTEGER PRIMARY KEY AUTOINCREMENT,\n  member_name TEXT,\n  member_email TEXT,\n  member_nickname TEXT,\n  member_phone TEXT,\n  gender TEXT,\n  birthday TEXT\n);",
            "code-interpreter": "Create the database table t_member, including the fields: member name, member email, member nickname, member mobile number, gender, birthday."
        },
        {
            "file-path": "src/main/java/com/aiassistant/model/Member.java",
            "reference-file": "src/main/java/com/aiassistant/model/Target.java",
            "code": "package com.aiassistant.model;\n\nimport lombok.Data;\n\n@Data\npublic class Member {\n  private Integer id;\n  private String memberName;\n  private String memberEmail;\n  private String memberNickname;\n  private String memberPhone;\n  private String gender;\n  private String birthday;\n}",
            "code-interpreter": "Adds a mapping of the membership management-related fields in the target entity class Member."
        },
        {
            "file-path": "src/main/java/com/aiassistant/mapper/MemberMapper.java",
            "reference-file": "src/main/java/com/aiassistant/mapper/TargetMapper.java",
            "code": "package com.aiassistant.mapper;\n\nimport com.aiassistant.model.Member;\nimport org.apache.ibatis.annotations.Insert;\nimport org.apache.ibatis.annotations.Mapper;\n\n@Mapper\npublic interface MemberMapper {\n  @Insert(\"INSERT INTO t_member (member_name, member_email, member_nickname, member_phone, gender, birthday) VALUES (#{memberName}, #{memberEmail}, #{memberNickname}, #{memberPhone}, #{gender}, #{birthday})\")\n  void addMember(Member member);\n}",
            "code-interpreter": "Adds a method to add a member to the target Mapper interface MemberMapper."
        },
        {
            "file-path": "src/main/resources/mapper/MemberMapper.xml",
            "reference-file": "src/main/resources/mapper/TargetMapper.xml",
            "code": "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n<!DOCTYPE mapper PUBLIC \"-//mybatis.org//DTD Mapper 3.0//EN\" \"http://mybatis.org/dtd/mybatis-3-mapper.dtd\">\n<mapper namespace=\"com.aiassistant.mapper.MemberMapper\">\n  <insert id=\"addMember\" parameterType=\"com.aiassistant.model.Member\">\n    INSERT INTO t_member (member_name, member_email, member_nickname, member_phone, gender, birthday)\n    VALUES (#{memberName}, #{memberEmail}, #{memberNickname}, #{memberPhone}, #{gender}, #{birthday})\n  </insert>\n</mapper>",
            "code-interpreter": "Add the SQL statement for adding a member to MemberMapper.xml in the SQL mapping file of the target Mapper interface."
        },
        {
            "file-path": "src/main/java/com/aiassistant/service/MemberService.java",
            "reference-file": "src/main/java/com/aiassistant/service/TargetService.java",
            "code": "package com.aiassistant.service;\n\nimport com.aiassistant.model.Member;\n\npublic interface MemberService {\n  void addMember(Member member);\n}",
            "code-interpreter": "Adds a method declaration for adding a member to the target Service interface MemberService."
        },
        {
            "file-path": "src/main/java/com/aiassistant/service/impl/MemberServiceImpl.java",
            "reference-file": "src/main/java/com/aiassistant/service/impl/TargetServiceImpl.java",
            "code": "package com.aiassistant.service.impl;\n\nimport com.aiassistant.mapper.MemberMapper;\nimport com.aiassistant.model.Member;\nimport com.aiassistant.service.MemberService;\nimport lombok.RequiredArgsConstructor;\nimport org.springframework.stereotype.Service;\n\n@Service\n@RequiredArgsConstructor\npublic class MemberServiceImpl implements MemberService {\n  private final MemberMapper memberMapper;\n\n  @Override\n  public void addMember(Member member) {\n    memberMapper.addMember(member);\n  }\n}",
            "code-interpreter": "The method to add a member is implemented in the target Service interface implementation class MemberServiceImpl."
        },
        {
            "file-path": "src/main/java/com/aiassistant/controller/MemberController.java",
            "reference-file": "src/main/java/com/aiassistant/controller/TargetController.java",
            "code": "package com.aiassistant.controller;\n\nimport com.aiassistant.model.Member;\nimport com.aiassistant.service.MemberService;\nimport io.swagger.annotations.Api;\nimport io.swagger.annotations.ApiOperation;\nimport lombok.RequiredArgsConstructor;\nimport org.springframework.web.bind.annotation.PostMapping;\nimport org.springframework.web.bind.annotation.RequestBody;\nimport org.springframework.web.bind.annotation.RequestMapping;\nimport org.springframework.web.bind.annotation.RestController;\n\n@RestController\n@RequestMapping(\"/members\")\n@Api(tags = \"Member Management\")\n@RequiredArgsConstructor\npublic class MemberController {\n  private final MemberService memberService;\n\n  @PostMapping\n  @ApiOperation(\"Add Member\")\n  public void addMember(@RequestBody Member member) {\n    memberService.addMember(member);\n  }\n}",
            "code-interpreter": "Adds an interface method for adding members to the target Controller."
        }
    ]
}]
