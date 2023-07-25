from app.extensions import db
import datetime
from app.controllers import register_controllers
from flask import Flask, request, session
from flask_cors import CORS
from app.models.task import getEmptyTaskInfo
from config import APP_SECRET_KEY, BACKEND_DEBUG, BACKEND_HOST, BACKEND_PORT, AICODER_ALLOWED_ORIGIN, AUTO_LOGIN

app = Flask(__name__)
CORS(app)
app.secret_key = APP_SECRET_KEY
app.config.from_pyfile('config.py')

@app.before_request
def require_login():
    if AUTO_LOGIN:
        if "username" not in session:
            session['logged_in'] = True
            session['username'] = "demo_user"
            session[session["username"]] = getEmptyTaskInfo()

    if request.path == '/user/language' or request.path == '/user/login':
        no = 1
    elif 'logged_in' not in session:
        return {'success': False, 'error': 'Access denied', 'code': 401}
    else:
        user = session["username"]
        current_time = datetime.datetime.now()
        path = request.path
        args = request.get_data(as_text=True)
        print(f"req_time: {current_time}")
        print(f"req_user: {user}")
        print(f"req_path: {path}")
        print(f"req_args: {args}")

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
