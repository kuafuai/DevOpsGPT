from flask import Blueprint, request, session
from app.controllers.common import json_response
from app.pkgs.tools.i18b import getI18n
from app.pkgs.tools.i18b import getFrontendText
from app.models.user import User
from app.models.user_pro import UserPro
from config import GRADE
from config import LANGUAGE

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/login', methods=['POST'])
@json_response
def login():
    _ = getI18n("controllers")
    data = request.json
    username = data['username']
    password = data['password']

    if GRADE == "base":
        ok = User.checkPassword(username, password)
    else:
        ok = UserPro.checkPassword(username, password)
        
    if ok:
        session['logged_in'] = True
        session['username'] = username
        return {'message': _('Login successful.')}
    else: 
        raise Exception("Invalid username or password")


@bp.route('/logout', methods=['POST'])
@json_response
def logout():
    _ = getI18n("controllers")
    session.clear()
    return {'message': _('Logout successful.')}

@bp.route('/change_language', methods=['GET'])
@json_response
def change_language():
    _ = getI18n("controllers")
    if "language" not in session:
        session['language'] = LANGUAGE
        session.update()
        
    if session['language'] == "zh":
        session['language'] = "en"
    else:
        session['language'] = "zh"
    session.update()

    return {'message': _('success.')}


@bp.route('/language', methods=['GET'])
@json_response
def language():
    if "language" not in session:
        session['language'] = LANGUAGE
        session.update()

    print(session)
    
    frontendText = getFrontendText() 

    return {"frontend_text": frontendText}