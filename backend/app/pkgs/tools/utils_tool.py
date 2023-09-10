import json
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import ssl
import uuid
import time
from datetime import datetime, timedelta

from app.pkgs.tools.llm import chatCompletion
from config import EMAIL_PASSWORD, EMAIL_PORT, EMAIL_SENDER, EMAIL_SERVER, EMAIL_SSL


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

def add_days_to_date(input_date_str, days_to_add):
    print("add_days_to_date")
    print(input_date_str)
    print(days_to_add)
    try:
        days_to_add = int(days_to_add)
        input_date = datetime.strptime(input_date_str, "%Y-%m-%d %H:%M:%S")
        new_date = input_date + timedelta(days=days_to_add)
        new_date_str = new_date.strftime("%Y-%m-%d %H:%M:%S")
        return True, new_date_str
    except Exception as e:
        return False, "无效的日期格式，请使用 'YYYY-MM-DD HH:MM:SS' 格式。" + str(e)

def if_datetime_expired(target_datetime_str):
    # 获取当前日期和时间
    current_datetime = datetime.now()

    # 将目标日期和时间字符串解析为datetime对象
    target_datetime = datetime.strptime(target_datetime_str, "%Y-%m-%d %H:%M:%S")

    # 比较两个日期和时间对象
    if current_datetime < target_datetime:
        return False
    else:
        return True

def send_email(receiver_email, subject, html_content):
    # 邮件服务器的信息
    smtp_server = EMAIL_SERVER
    smtp_port = EMAIL_PORT

    # 发件人和收件人信息
    sender_email = EMAIL_SENDER
    password = EMAIL_PASSWORD

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }

        .container {
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            padding: 20px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
            border-radius: 5px;
        }

        .header {
            text-align: center;
            padding: 20px 0;
        }

        .header h1 {
            color: #333;
            margin: 0;
        }

        .content {
            padding: 20px 0;
        }

        .footer {
            text-align: center;
            padding: 20px 0;
            color: #888;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>"""+subject+"""</h1>
        </div>
        <div class="content">
            """+html_content+"""
        </div>
        <div class="footer">
            <p>本邮件为系统邮件，请勿回复。This email is a system email, please do not reply.</p>
            <p>如有疑问，请添加我们的公众号：KuafuAI</p>
        </div>
    </div>
</body>
</html>

"""

    html_part = MIMEText(html, 'html')
    msg.attach(html_part)

    # 建立与邮件服务器的连接并发送邮件
    try:
        if EMAIL_SSL:
           context = ssl.create_default_context()
           server = smtplib.SMTP_SSL(smtp_server, smtp_port, context=context)
        else:
            server = smtplib.SMTP(smtp_server, smtp_port)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("邮件发送成功")
        return True
    except Exception as e:
        print(f"邮件发送失败: {e}")
        return False
