import json
from app.pkgs.tools.llm import chatCompletion
from app.pkgs.tools.i18b import getCurrentLanguageName
from app.pkgs.tools.utils_tool import fix_llm_json_str, get_code_from_str
from app.pkgs.prompt.code_interface import CodeInterface

class CodeBasic(CodeInterface):
    def aiReferenceRepair(self, requirementID, newCode, referenceCode, fileTask, filePath):
        prompt = f"""
    As a senior full stack developer. Your task is to analyze the following "reference code" style and specification (including but not limited to: naming conventions, coding styles, import package specifications, comment specifications, etc.) line by line, and use this to correct the "development task corresponding code" with the "reference code" style and specification is inconsistent. Ensure that the newly generated code can conform to the overall code style and specification of the program as well as the reference code without compromising the "development task". The consolidated code responds according to the response format example.

    reference code:
    ```
    """+referenceCode+""""
    ```

    development task：
    ```
    """+fileTask+"""
    ```

    development task corresponding code:
    ```
    """+newCode+"""
    ```

    You should only directly respond in JSON format as described below, Ensure the response must can be parsed by Python json.loads, Response Format example:
    {"reasoning": "{Explain the thought process of the problem step by step}","code": "{Optimized final complete code}"}

    Please respond in """+getCurrentLanguageName()+"""".
    """

        context = [{"role": "user", "content": prompt}]
        data, total_tokens, success = chatCompletion(context)
        return json.loads(fix_llm_json_str(data)), success


    def aiAnalyzeError(self, requirementID, message, filePath):
        prompt = f"""
    As a senior full stack developer. Your task is to analyze code execution error messages, return files that may need to be modified, and analyze the solution. Follow the response format example.

    error messages:
    ```
    """+message+"""
    ```

    You should only directly respond in JSON format as described below, Ensure the response must can be parsed by Python json.loads, Response Format example:
    [{"file-path": "file-path", "solution-analysis":"solution-analysis"}]

    Please respond in """+getCurrentLanguageName()+"""".
    """

        context = [{"role": "user", "content": prompt}]
        data, total_tokens, success = chatCompletion(context)
        return json.loads(fix_llm_json_str(data)), success


    def aiFixError(self, requirementID, error_msg, solution, code, filePath, type):
        prompt = f"""
    As a senior full stack developer. Your task is to fix errors in the "initial code". Please fix the problems in the "initial code" according to the solution, taking care not to affect other code functions. The consolidated code responds according to the response format example.

    initial code:
    ```
    """+code+"""
    ```

    solution:
    ```
    """+solution+"""
    ```

    error msg:
    ```
    """+error_msg+"""
    ```

    You should only directly respond in JSON format as described below, Ensure the response must can be parsed by Python json.loads, Response Format example:
    {"reasoning": "{Explain the thought process of the problem step by step"}","code": "{Optimized final complete code or initial code}"}

    Please respond in """+getCurrentLanguageName()+"""".
    """

        context = [{"role": "user", "content": prompt}]
        data, total_tokens, success = chatCompletion(context)
        return json.loads(fix_llm_json_str(data)), success


    def aiCheckCode(self, requirementID, fileTask, code, filePath, service_name):
        goodCodeRe, success = self.aiReviewCode(requirementID, fileTask, code, filePath)

        jsonData = {"reasoning": goodCodeRe, "code": code}

        prompt = f"""
NOTICE
Role: As a senior full stack developer, you are task is to modify the code according to the modification suggestions. 

Think step by step and reason yourself to the right decisions to make sure we get it right.

original code:
```
"""+code+"""
```

Modification suggestion:
```
"""+goodCodeRe+"""
```

Please return the final code according to the modification suggestion, the final code should be fully functional, finish all implementation details without omitted. No placeholders no todo, ensure that all code can run in production environment correctly.
Do not explain and talk, directly respond the final complete executable code.
The response must be code.
        """

        context = [{"role": "user", "content": prompt}]
        data, total_tokens, success = chatCompletion(context)
        newCode = get_code_from_str(data)
        if len(newCode) < len(code)/3*2:
            jsonData["code"] = code
        else:
            jsonData["code"] = newCode

        return jsonData, success
    
    def aiReviewCode(self, requirementID, fileTask, code, filePath):
        prompt = f"""
NOTICE
Role: You are a professional software engineer, Your task is to review the code. 

code:
```
"""+code+"""
```

development task:
```
"""+fileTask+"""
```

Check the code item by item for the checklist below
This code is very important and you will review it carefully
```
1. Is the code implemented as per the development task?
2. Is the code contains errors or contains issues with the code logic?
3. Is there a function in the code that is omitted or not fully implemented that needs to be implemented?(For example, only placeholders\comment\pass are written in the code but no specific code is written)?
```
    """

        context = [{"role": "user", "content": prompt}]
        data, total_tokens, success = chatCompletion(context)

        return data, success


    def aiMergeCode(self, requirementID, task, baseCode, newCode, filePath):
        prompt = f"""
    As a senior full stack developer. Your task is to integrate with existing code according to the "Development Task" and "Development Task corresponding code" provided below. In the process of integrating code, you must use the existing code as a baseline, and always be careful to ensure that the functionality of the existing code body is not affected. The consolidated code responds according to the response format example.

    Development Task:
    ```
    """+task+"""
    ```

    Development Task corresponding code:
    ```
    """+newCode+"""
    ```

    existing code:
    ```
    """+baseCode+"""
    ```

    You should only directly respond in JSON format as described below, Ensure the response must can be parsed by Python json.loads, Response Format example:
    {"reasoning": "{Explain the thought process of the problem step by step}","code": "{Optimized final complete code}"}

    Please respond in """+getCurrentLanguageName()+"""".
    """

        context = [{"role": "user", "content": prompt}]
        data, total_tokens, success = chatCompletion(context)
        return json.loads(fix_llm_json_str(data)), success


    def aiGenCode(self, requirementID, fileTask, newTask, newCode, filePath):
        prompt = f"""
    As a senior full stack developer. you need to modify the "basic code" based on the "change suggestions" and return all the complete code that works well. The code style is consistent with the "base code", try not to break the original function.

    change suggestions:
    ```
    """+newTask+"""
    ```

    basic code:
    ```
    """+newCode+"""
    ```

    You should only directly respond in JSON format as described below
    Response Format example:
    {"reasoning": "{Explain the thought process of the problem step by step}","code": "{Optimized final complete code}"}
    Ensure the response must can be parsed by Python json.loads

    Please respond in """+getCurrentLanguageName()+"""".
    """

        context = [{"role": "user", "content": prompt}]
        data, total_tokens, success = chatCompletion(context)
        return json.loads(fix_llm_json_str(data)), success
