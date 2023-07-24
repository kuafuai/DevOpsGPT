import threading
import time
import openai
from config import LLM_MODEL
from config import GPT_KEYS

api_keys = GPT_KEYS

api_key_index = 0
lock = threading.Lock()

def get_next_api_key():
    print("get_next_api_key:", flush=True)
    print(api_keys, flush=True)
    global api_key_index
    current_time = int(time.time())
    with lock:
        key = list(api_keys.keys())[api_key_index]
        key_data = api_keys[key]
        if current_time - key_data["timestamp"] >= 80:
            key_data["count"] = 0
            key_data["timestamp"] = current_time
            api_key_index = (api_key_index + 1) % len(api_keys)
            return key
        elif key_data["count"] < 2:
            key_data["count"] += 1
            api_key_index = (api_key_index + 1) % len(api_keys)
            return key
    time.sleep(80)
    return get_next_api_key()

def chartGPT(msg_current):
    print("chartGPT - message:", flush=True)
    print(msg_current, flush=True)
    openai.api_key = get_next_api_key()
    print("chartGPT - get api key:"+openai.api_key, flush=True)

    response = openai.ChatCompletion.create(
        model= LLM_MODEL,
        messages=msg_current,
        max_tokens=12000,
        temperature=0,
    )

    response_text = response["choices"][0]["message"]["content"]
    print("chartGPT - response_text:"+response_text, flush=True)
    return response_text, True