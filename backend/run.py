from app.extensions import db
from app.flask_ext import limiter_ip
import datetime
from app.controllers import register_controllers
from flask import Flask, request
from flask_cors import CORS
from app.models.tenant_pro import Tenant
from app.pkgs.tools import storage
from app.pkgs.scheduler import register_job
from config import APP_SECRET_KEY, BACKEND_DEBUG, BACKEND_HOST, BACKEND_PORT, AICODER_ALLOWED_ORIGIN, AUTO_LOGIN, GRADE

import logging
import os
from apscheduler.schedulers.background import BackgroundScheduler

aps_logger = logging.getLogger('apscheduler')
aps_logger.setLevel(logging.ERROR)

app = Flask(__name__)
CORS(app)
app.secret_key = APP_SECRET_KEY
app.config.from_pyfile('config.py')

NOT_CHECK_LOGIN_PATH = [
    '/user/send_launch_code',
    '/user/language',
    '/user/change_language',
    '/user/login',
    '/user/changepassword',
    '/user/logout',
    '/user/register',
    '/pay/get_price',
    '/pay/send_pay',
    '/tenant/join',
    '/tenant/get_all_tenant',
    '/plugine/repo_analyzer',
    '/plugine/repo_analyzer_check',
    '/tencent/shop_create_item'
]


@app.before_request
def require_login():
    # 开启自动登录，直接设置
    if AUTO_LOGIN:
        storage.set("username", "demo_user")
        storage.set("user_id", 1)
        storage.set("tenant_id", 0)

    path = request.path
    # 不需要验证登录状态的接口
    if path in NOT_CHECK_LOGIN_PATH:
        pass
    # 如果未登录返回错误
    elif not storage.get("username") or not storage.get("user_id"):
        return {'success': False, 'error': 'Access denied', 'code': 401}
    # 如果登录了，验证组织状态和是否有操作权限
    else:
        username = storage.get("username")
        current_time = datetime.datetime.now()
        args = request.get_data(as_text=True)
        print(f"req_time: {current_time}")
        print(f"req_user: {username}")
        print(f"req_path: {path}")
        print(f"req_args: {args}")

        if GRADE != "base":
            issuccess, msg, code = Tenant.check_status_and_role(request, path)
            if not issuccess:
                return {'success': False, 'error': msg, 'code': code}


@app.after_request
def after_request(response):
    origin = request.headers.get("Origin")
    if origin in AICODER_ALLOWED_ORIGIN:
        response.headers.add('Access-Control-Allow-Origin', origin)
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response


limiter_ip.init_app(app)

register_controllers(app)

db.init_app(app)

if os.environ.get('WERKZEUG_RUN_MAIN') != 'true' and GRADE != 'base':
    print("init scheduler")
    scheduler = BackgroundScheduler(daemon=True)
    register_job(scheduler, app)
    scheduler.start()

if __name__ == '__main__':
    app.run(host=BACKEND_HOST, port=BACKEND_PORT, debug=BACKEND_DEBUG)
