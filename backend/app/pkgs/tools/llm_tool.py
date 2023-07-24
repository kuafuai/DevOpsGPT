import traceback
from app.pkgs.tools.llm_tool_chatgpt import chartGPT
from app.pkgs.tools.llm_tool_pro import multiGPT
from config import GRADE

def askLLM(context):
    message = "" 
    success = False
    try:
        if GRADE == 'base':
            message, success = chartGPT(context)
        else:
            message, success = multiGPT(context)
    except Exception as e:
        print("askLLM failed first time:" + str(e))
        try:
            if GRADE == 'base':
                message, success = chartGPT(context)
            else:
                message, success = multiGPT(context)
        except Exception as e:
            print("askLLM failed second time:" + str(e))
            traceback.print_exc()
            message = ""
            success = False
    return message, success