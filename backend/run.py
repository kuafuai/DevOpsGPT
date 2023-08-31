from app.extensions import db
import datetime
from app.controllers import register_controllers
from flask import Flask, request, session, abort
from flask_cors import CORS
from app.models.task import getEmptyTaskInfo
from app.models.tenant_pro import Tenant
from app.models.tenant_user_pro import TenantUser
from app.models.user_pro import UserPro
from config import APP_SECRET_KEY, BACKEND_DEBUG, BACKEND_HOST, BACKEND_PORT, AICODER_ALLOWED_ORIGIN, AUTO_LOGIN, GRADE

app = Flask(__name__)
CORS(app)
app.secret_key = APP_SECRET_KEY
app.config.from_pyfile('config.py')

@app.before_request
def require_login():
    if AUTO_LOGIN:
        if "username" not in session:
            session['username'] = "demo_user"
            session['tenant_id'] = 0
            session[session["username"]] = getEmptyTaskInfo()
    path = request.path

    if path == '/user/language' or path == '/user/login' or path == '/user/logout' or path == '/user/change_language' or path == '/user/register':
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
            current_path = request.args.get('url_path')
            if (current_path == "/tenant.html" or current_path == "/tenant_new.html") and path=="/requirement/clear_up":
                pass
            elif path =="/tenant/create" or path=="/tenant/get_all" or path=="/tenant/use_tenant":
                pass
            else:
                success, msg, code = check_tenant_membership_and_permissions()
                if not success:
                    return {'success': False, 'error': msg, 'code': code}

def check_tenant_membership_and_permissions():
    username = session["username"]
    user = UserPro.get_user_by_name(username)
    tenant_id = session['tenant_id']
    success, msg = Tenant.check_tenant(tenant_id)
    print("check_tenant_membership_and_permissions:")
    print(tenant_id)
    print(msg)
    print(success)
    if not success:
        return success, msg, 404
    
    success, msg = TenantUser.check_role(user["user_id"], tenant_id, request.path)
    if not success:
        return success, msg, 403
    
    return success, msg, 200


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
