import os

from config import WORKSPACE_PATH


def read_file_content(filename):
    print("read_file_content:" + filename)
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            result = True
    except FileNotFoundError:
        content = ''
        result = False
    return result, content


def write_file_content(filename, content):
    print("write_file_content:" + filename)
    directory = os.path.dirname(filename)
    os.makedirs(directory, exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)


def get_ws_path(task_id):
    return WORKSPACE_PATH + task_id
