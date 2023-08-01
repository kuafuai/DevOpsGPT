import traceback
from app.pkgs.tools.llm_pro import LLMPro
from app.pkgs.tools.llm_basic import LLMBase
from config import GRADE

def chatCompletion(context):
    if GRADE == "base":
        obj = LLMBase()
    else:
        obj = LLMPro()

    message = "" 
    success = False
    try:
        message, success = obj.chatCompletion(context)
    except Exception as e:
        print("chatCompletion failed first time:" + str(e))
        try:
            message, success = obj.chatCompletion(context)
        except Exception as e:
            print("chatCompletion failed second time:" + str(e))
            traceback.print_exc()
            message = ""
            success = False
    return message, success