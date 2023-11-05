import json
import random
import re
import uuid
import time
from datetime import datetime, timedelta
from app.pkgs.tools.llm import chatCompletion


def detect_programming_language(file_path):
    file_extension = file_path.split('.')[-1]

    language_extensions = {
        'Python': ['py'],
        'JavaScript': ['js'],
        'Java': ['java'],
        'C++': ['cpp', 'cxx', 'cc'],
        'C': ['c'],
        'Ruby': ['rb'],
        'Go': ['go'],
        'Swift': ['swift'],
    }

    for language, extensions in language_extensions.items():
        if file_extension.lower() in extensions:
            return language

    return 'Unknown'

def get_last_n_lines(text, need_lens):
    lines = text.split('\n')
    lines_count = len(lines)

    if lines_count < need_lens:
        return text

    last_10_lines = lines[-1*need_lens:]
    result = '\n'.join(last_10_lines)
    return result

def fix_llm_json_str(string):
    new_string = string.strip()
    try:
        json.loads(new_string)
        return new_string
    except Exception as e:
        print("fix_llm_json_str failed 1:", e)
        try:
            pattern = r'```json(.*?)```'
            match = re.findall(pattern, new_string, re.DOTALL)
            if match:
                new_string = match[-1]
            
            json.loads(new_string)
            return new_string
        except Exception as e:
            print("fix_llm_json_str failed 2:", e)
            try:
                new_string = new_string.replace("\n", "\\n")
                json.loads(new_string)
                return new_string
            except Exception as e:
                print("fix_llm_json_str failed 3:", e)
                
                ctx = [{
                    "role": "system",
                    "content": """Do not change the specific content, fix the json, directly return the repaired JSON, without any explanation and dialogue.
                    ```
                    """+new_string+"""
                    ```"""
                }]

                message, total_tokens, success = chatCompletion(ctx)
                pattern = r'```json(.*?)```'
                match = re.findall(pattern, message, re.DOTALL)
                if match:
                    return match[-1]

                return message

def get_code_from_str(input_string):
    # 定义正则表达式模式
    pattern = r"```.*?\n(.*?)```"
    # 使用re模块进行匹配
    matches = re.findall(pattern, input_string, re.DOTALL)
    output_string = input_string
    # 输出匹配结果
    for match in matches:
        if len(match) > 0:
            output_string = match


    # 定义正则表达式模式
    pattern = r"```(.*?)```"
    # 使用re模块进行匹配
    matches = re.findall(pattern, output_string, re.DOTALL)
    # 输出匹配结果
    for match in matches:
        if len(match) > 0:
            output_string = match

    return output_string

def generate_uuid():
    # 生成一个UUID
    uuid_value = uuid.uuid4()
    
    # 获取当前时间的毫秒级时间戳
    timestamp = int(time.time() * 1000)
    
    # 将时间戳转换为16进制字符串
    timestamp_hex = hex(timestamp)[2:]
    
    # 将时间戳添加到UUID的末尾
    time_uuid = f"{uuid_value}-{timestamp_hex}"
    
    return time_uuid

def generate_launch_code():
    return str(random.randint(100000, 999999))

def add_days_to_date(input_date_str, days_to_add):
    print("add_days_to_date")
    print(input_date_str)
    print(days_to_add)
    try:
        if isinstance(input_date_str, datetime):
            input_date_str = input_date_str.strftime('%Y-%m-%d %H:%M:%S')

        days_to_add = int(days_to_add)
        input_date = datetime.strptime(input_date_str, "%Y-%m-%d %H:%M:%S")
        new_date = input_date + timedelta(days=days_to_add)
        new_date_str = new_date.strftime("%Y-%m-%d %H:%M:%S")
        return True, new_date_str
    except Exception as e:
        print("add_days_to_date failed: "+ str(e))
        return False, "无效的日期格式，请使用 'YYYY-MM-DD HH:MM:SS' 格式。" + str(e)

def if_datetime_expired(target_datetime_str):
    try:
        if isinstance(target_datetime_str, datetime):
            target_datetime_str = target_datetime_str.strftime('%Y-%m-%d %H:%M:%S')

        # 获取当前日期和时间
        current_datetime = datetime.now()

        # 将目标日期和时间字符串解析为datetime对象
        target_datetime = datetime.strptime(target_datetime_str, "%Y-%m-%d %H:%M:%S")

        # 比较两个日期和时间对象
        if current_datetime < target_datetime:
            return False
        else:
            return True
    except Exception as e:
        print("if_datetime_expired error:"+str(e))
        return True

def hide_half_str(input_string):
    # 如果输入字符串长度小于2，返回全部星号
    if len(input_string) < 2:
        return '*' * len(input_string)

    # 计算要隐藏的字符数，这是字符串长度的一半
    num_to_hide = len(input_string) // 2

    # 生成星号替换字符串
    asterisks = '*' * num_to_hide

    # 将星号替换字符串与原字符串的前半部分组合起来
    result = input_string[:num_to_hide] + asterisks

    return result

def is_valid_email(email):
    # 定义邮箱地址的正则表达式模式
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    
    # 使用re.match()来检查邮箱是否匹配模式
    if re.match(pattern, email):
        return True
    else:
        return False
    
def is_valid_username(username):
    # 使用正则表达式匹配用户名
    pattern = r'^[a-zA-Z0-9_-]+$'
    if re.match(pattern, username):
        return True
    else:
        return False