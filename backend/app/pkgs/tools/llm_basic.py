import threading
import time
import openai
from app.pkgs.tools.llm_interface import LLMInterface
from config import MODE, LLM_MODEL, GPT_KEYS

api_keys = GPT_KEYS

api_key_index = 0
provider_index = 0
lock = threading.Lock()

def get_next_api_key():
    print("get_next_api_key:", flush=True)
    print(api_keys, flush=True)
    global api_key_index, provider_index
    current_time = int(time.time())
    with lock:
        provider = list(api_keys.keys())[provider_index]
        provider_data = api_keys[provider]
        keys = provider_data["keys"]
        key_data = keys[api_key_index]
        key = list(key_data.keys())[0]
        if current_time - key_data[key]["timestamp"] >= 80:
            key_data[key]["count"] = 0
            key_data[key]["timestamp"] = current_time
            api_key_index = (api_key_index + 1) % len(keys)
            if api_key_index == 0:
                provider_index = (provider_index + 1) % len(api_keys)
            return provider_data, key
        elif key_data[key]["count"] < 2:
            key_data[key]["count"] += 1
            api_key_index = (api_key_index + 1) % len(keys)
            if api_key_index == 0:
                provider_index = (provider_index + 1) % len(api_keys)
            return provider_data, key
    time.sleep(80)
    return get_next_api_key()

class LLMBase(LLMInterface):
    def chatCompletion(self, context, fackData, bill):
        # Test frontend
        if MODE == "FAKE" and len(fackData) > 0:
            time.sleep(5)
            return fackData, True
        
        print("chatGPT - message:", flush=True)
        print(context, flush=True)
        provider_data, key = get_next_api_key()
        if len(key) < 10:
            print(f"\n\033[91mError: The GPT_KEYS({key}) in env.yaml is incorrectly, please modify the configuration according to the configuration notes. \033[0m\n")
            exit(1)
        
        openai.api_key = key
        openai.api_type = provider_data["api_type"]
        openai.api_base = provider_data["api_base"]
        openai.api_version = provider_data["api_version"]
        openai.proxy = None if provider_data["proxy"]=="None" else provider_data["proxy"]
        print("chatGPT - get api key:"+openai.api_key, flush=True)
        print(f"provider_data:{provider_data}")

        try:
            response = openai.ChatCompletion.create(
                model= LLM_MODEL,
                deployment_id = provider_data.get("deployment_id", None),
                messages=context,
                max_tokens=10000,
                temperature=0,
            )

            response_text = response["choices"][0]["message"]["content"]
            total_tokens = response["usage"]["total_tokens"]
            print("chatGPT - response_text:"+response_text, flush=True)
            return response_text, total_tokens, True
        except Exception as e:
            msg = "\nError: Failed to access GPT, please check whether your network can connect to GPT and terminal proxy is running properly.\n"
            print(f"\033[91m{msg} \033[0m")
            raise e
