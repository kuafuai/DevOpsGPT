from flask_limiter import Limiter
from flask import request
from flask_limiter.util import get_remote_address


def limit_ip_func():
    ip = str(request.headers.get("X-Forwarded-For", '127.0.0.1'))
    print(ip, get_remote_address())
    return ip


limiter_ip = Limiter(key_func=limit_ip_func)
