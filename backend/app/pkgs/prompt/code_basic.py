import json
from app.pkgs.tools.llm import chatCompletion
from app.pkgs.tools.i18b import getCurrentLanguageName
from app.pkgs.tools.utils_tool import fix_llm_json_str
from app.pkgs.prompt.code_interface import CodeInterface
from config import GRADE

class CodeBasic(CodeInterface):
    def aiReferenceRepair(self, newCode, referenceCode, fileTask):
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

    Use """+getCurrentLanguageName()+"""" dialogue
    """

        context = [{"role": "user", "content": prompt}]
        data, success = chatCompletion(context)
        return json.loads(fix_llm_json_str(data)), success


    def aiAnalyzeError(self, message):
        prompt = f"""
    As a senior full stack developer. Your task is to analyze code execution error messages, return files that may need to be modified, and analyze the solution. Follow the response format example.

    error messages:
    ```
    """+message+"""
    ```

    You should only directly respond in JSON format as described below, Ensure the response must can be parsed by Python json.loads, Response Format example:
    [{"file-path": "file-path", "solution-analysis":"solution-analysis"}]

    Note: Keep conversations in """+getCurrentLanguageName()+""".
    """

        context = [{"role": "user", "content": prompt}]
        data, success = chatCompletion(context)
        return json.loads(fix_llm_json_str(data)), success


    def aiFixError(self, solution, code):
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

    You should only directly respond in JSON format as described below, Ensure the response must can be parsed by Python json.loads, Response Format example:
    {"reasoning": "{Explain the thought process of the problem step by step"}","code": "{Optimized final complete code or initial code}"}

    Use """+getCurrentLanguageName()+"""" dialogue
    """

        context = [{"role": "user", "content": prompt}]
        data, success = chatCompletion(context)
        return json.loads(fix_llm_json_str(data)), success


    def aiCheckCode(self, fileTask, code):
        prompt = f"""
    As a senior full stack developer. Your task is to check whether the following "initial code" has obvious syntax errors. If there is a problem in the "initial code", please fix the code if not just return the "initial code" as is. The consolidated code responds according to the response format example.

    initial code:
    ```
    """+code+"""
    ```

    development task:
    ```
    """+fileTask+"""
    ```

    You should only directly respond in JSON format as described below, Ensure the response must can be parsed by Python json.loads, Response Format example:
    {"reasoning": "{Explain the thought process of the problem step by step}","code": "{Optimized final complete code or initial code}"}

    Use """+getCurrentLanguageName()+"""" dialogue
    """

        context = [{"role": "user", "content": prompt}]
        data, success = chatCompletion(context)
        return json.loads(fix_llm_json_str(data)), success


    def aiMergeCode(self, task, baseCode, newCode):
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

    Use """+getCurrentLanguageName()+"""" dialogue
    """

        context = [{"role": "user", "content": prompt}]
        data, success = chatCompletion(context)
        return json.loads(fix_llm_json_str(data)), success


    def aiGenCode(self, fileTask, newTask, appName, newCode):
        prompt = f"""
    As a senior full stack developer. you need to modify the "basic code" based on the "change suggestions" and return all the complete code that works well. The code style is consistent with the "base code", do not destroy the original function. 

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

    Use """+getCurrentLanguageName()+"""" dialogue
    """

        context = [{"role": "user", "content": prompt}]
        data, success = chatCompletion(context)
        return json.loads(fix_llm_json_str(data)), success
