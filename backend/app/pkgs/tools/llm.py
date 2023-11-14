import traceback
from app.pkgs.tools.llm_pro import LLMPro
from app.pkgs.tools.llm_basic import LLMBase
from config import GRADE

def chatCompletion(context, fackData="", bill: bool = True):
    if GRADE == "base":
        obj = LLMBase()
    else:
        obj = LLMPro()

    message = "" 
    success = False
    try:
        message, total_tokens, success = obj.chatCompletion(context, fackData, bill)
    except Exception as e:
        print("chatCompletion failed 1 time:" + str(e))
        try:
            message, total_tokens, success = obj.chatCompletion(context, fackData, bill)
        except Exception as e:
            print("chatCompletion failed 2 time:" + str(e))
            traceback.print_exc()
            try:
                message, total_tokens, success = obj.chatCompletion(context, fackData, bill)
            except Exception as e:
                print("chatCompletion failed 3 time:" + str(e))
                traceback.print_exc()
                try:
                    message, total_tokens, success = obj.chatCompletion(context, fackData, bill)
                except Exception as e:
                    print("chatCompletion failed 4 time:" + str(e))
                    traceback.print_exc()
                    try:
                        message, total_tokens, success = obj.chatCompletion(context, fackData, bill)
                    except Exception as e:
                        print("chatCompletion failed 5 time:" + str(e))
                        traceback.print_exc()
                        try:
                            message, total_tokens, success = obj.chatCompletion(context, fackData, bill)
                        except Exception as e:
                            print("chatCompletion failed 6 time:" + str(e))
                            traceback.print_exc()
                            raise Exception("服务异常，请重试。Service exception, please try again.")
    return message, total_tokens, success