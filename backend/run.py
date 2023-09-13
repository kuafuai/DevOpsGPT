from app.extensions import db
import datetime
from app.controllers import register_controllers
from flask import Flask, request, session
from flask_cors import CORS
from app.models.task import getEmptyTaskInfo
from app.models.tenant_pro import Tenant
from app.models.tenant_user_pro import TenantUser
from config import APP_SECRET_KEY, BACKEND_DEBUG, BACKEND_HOST, BACKEND_PORT, AICODER_ALLOWED_ORIGIN, AUTO_LOGIN, GRADE

app = Flask(__name__)
CORS(app)
app.secret_key = APP_SECRET_KEY
app.config.from_pyfile('config.py')

@app.before_request
def require_login():
    if AUTO_LOGIN and GRADE == "base":
        if "username" not in session:
            session['username'] = "demo_user"
            session['user_id'] = 1
            session['tenant_id'] = 0
            session[session["username"]] = getEmptyTaskInfo()

    path = request.path
    if path == '/user/send_launch_code' or path == '/user/language' or path == '/user/login' or path == '/user/logout' or path == '/user/change_language' or path == '/user/register':
        pass
    elif 'username' not in session:
        return {'success': False, 'error': 'Access denied', 'code': 401}
    else:
        user = session["username"]
        current_time = datetime.datetime.now()
        args = request.get_data(as_text=True)
        print(f"req_time: {current_time}")
        print(f"req_user: {user}")
        print(f"req_path: {path}")
        print(f"req_args: {args}")
        
        if GRADE != "base":
            try:
                tenant_id = request.args.get('tenant_id')
                if not tenant_id:
                    tenant_id = session['tenant_id']
            except Exception as e:
                tenant_id = 0

            # If not on the company management page, determine the company status
            if not path.startswith("/tenant/") and path != "/requirement/clear_up" and not path.startswith("/pay/"):
                success, msg = Tenant.check_tenant(tenant_id)
                if not success:
                    return {'success': False, 'error': msg, 'code': 404}
            # authority check
            success, msg = TenantUser.check_role(session['user_id'], tenant_id, path)
            if not success:
                return {'success': False, 'error': msg, 'code': 403}

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', AICODER_ALLOWED_ORIGIN) 
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response

register_controllers(app)

db.init_app(app)

if __name__ == '__main__':
    app.run(host=BACKEND_HOST, port=BACKEND_PORT, debug=BACKEND_DEBUG)
