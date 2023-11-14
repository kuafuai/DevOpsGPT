from flask_limiter import Limiter
from flask import request
from flask_limiter.util import get_remote_address


def limit_ip_func():
    ip = str(request.headers.get("X-Forwarded-For", '127.0.0.1'))
    remote_ip = get_remote_address()

    print("limit ip : ", ip, remote_ip)

    if ip != '127.0.0.1':
        return ip

    if remote_ip != '127.0.0.1':
        return remote_ip

    return '127.0.0.1'


limiter_ip = Limiter(key_func=limit_ip_func)
