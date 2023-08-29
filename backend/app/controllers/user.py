from flask import Blueprint, request, session
from app.controllers.common import json_response
from app.pkgs.tools.i18b import getI18n
from app.pkgs.tools.i18b import getFrontendText
from app.models.user import User
from app.models.user_pro import UserPro
from config import GRADE
from config import LANGUAGE

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/register', methods=['POST'])
@json_response
def register():
    _ = getI18n("controllers")
    data = request.json
    username = data['username']
    password = data['password']
    email = data['email']
    phone_number = data['phone']
    zone_language = LANGUAGE
    if "language" in session:
        zone_language = session['language']

    if GRADE == "base":
        raise Exception("The current version does not support this feature")
    else:
        # todo 0
        current_tenant = 0
        user = UserPro.create_user(username, password, phone_number, email, zone_language, current_tenant)
        
        return user.username

@bp.route('/login', methods=['POST'])
@json_response
def login():
    _ = getI18n("controllers")
    data = request.json
    username = data['username']
    password = data['password']

    if GRADE == "base":
        ok = User.checkPassword(username, password)
        session['tenant_id'] = 0
    else:
        ok = UserPro.checkPassword(username, password)
        if ok:
            userinfo = UserPro.get_user_by_name(username)
            session['language'] = userinfo["zone_language"]
            session['tenant_id'] = userinfo["current_tenant"]
        
    if ok:
        session['logged_in'] = True
        session['username'] = username        
        return {'message': _('Login successful.')}
    else: 
        raise Exception(_("Invalid username or password"))


@bp.route('/logout', methods=['POST'])
@json_response
def logout():
    _ = getI18n("controllers")
    language = LANGUAGE
    if "language" in session:
        language = session['language']
    session.clear()
    session['language'] = language
    session.update()
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

    if GRADE != "base" and "username" in session:
        username = session['username']
        userinfo = UserPro.get_user_by_name(username)
        UserPro.update_user(userinfo["user_id"], zone_language=session['language'])

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