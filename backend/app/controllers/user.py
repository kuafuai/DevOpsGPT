from flask import Blueprint, request, session
from app.controllers.common import json_response
from app.pkgs.tools.i18b import getI18n
from app.pkgs.tools.i18b import getFrontendText
from app.models.user import User
from app.models.user_pro import UserPro
from app.models.tenant_user_pro import TenantUser
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
        current_tenant = 0
        tus = TenantUser.get_tenant_user_by_invite_email(email)
        for tu in tus:
            current_tenant = tu["tenant_id"]
        
        user = UserPro.create_user(username, password, phone_number, email, zone_language, current_tenant)
        
        for tu in tus:
            TenantUser.active_tenant_user(tu["tenant_user_id"], user.user_id)
        
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
        session['user_id'] = 1
        session['username'] = username 
    else:
        ok = UserPro.checkPassword(username, password)
        if ok:
            userinfo = UserPro.get_user_by_name(username)
            session['language'] = userinfo["zone_language"]

            session['tenant_id'] = userinfo["current_tenant"]
            session['user_id'] = userinfo["user_id"]
            session['username'] = username 
        
    if ok:
        return {'message': _('Login successful.')}
    else: 
        raise Exception(_("Invalid username or password"))


@bp.route('/logout', methods=['GET'])
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