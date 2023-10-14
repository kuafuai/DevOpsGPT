from datetime import datetime
from flask import Blueprint, request
from app.pkgs.tools import storage
from app.controllers.common import json_response
from app.pkgs.tools.i18b import getI18n
from app.pkgs.tools.i18b import getFrontendText
from app.models.user import User
from app.models.user_pro import UserPro
from app.models.tenant_user_pro import TenantUser
from app.models.user_pro import gen_launch_code
from app.models.tenant_pro import Tenant
from app.pkgs.tools.utils_tool import add_days_to_date
from config import GRADE
from config import LANGUAGE, INVITATION_CODE

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
    launch_code = data['launch_code']
    invitation_code = data['invitation_code']
    zone_language = LANGUAGE
    if storage.get("language"):
        zone_language = storage.get("language")

    if GRADE == "base":
        raise Exception("The current version does not support this feature")
    else:
        if invitation_code != INVITATION_CODE:
            raise Exception(_("invitation code not right (Thank you for your interest. We will open registration after the beta testing phase.)"))
        current_tenant = 0
        tus = TenantUser.get_tenant_user_by_invite_email(email)
        for tu in tus:
            current_tenant = tu["tenant_id"]
        
        user = UserPro.create_user(username, password, phone_number, email, zone_language, current_tenant, launch_code)
        
        # 激活所有被邀请的企业成员
        if user:
            # 自动创建一个个人租户
            # 免费赠送14天基础会员
            from_data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            success, billing_end = add_days_to_date(from_data, 14)

            tenant = Tenant.create_tenant_with_codepower(username + _("'s personal Organization"), Tenant.STATUS_PendingVerification, username, "", "", "", Tenant.BILLING_TYPE_BASIC_MONTHLY, Tenant.BILLING_QUOTA_5, billing_star=None, billing_end=billing_end, user_id=user.user_id, username=email)

            current_tid = tenant.tenant_id

            for tu in tus:
                current_tid = tu["tenant_id"]
                TenantUser.active_tenant_user(tu["tenant_user_id"], user.user_id)

            UserPro.update_user(user.user_id, current_tenant=current_tid)
        
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
        storage.set("tenant_id", 0) 
        storage.set("user_id", 1) 
        storage.set("username", username)
    else:
        ok = UserPro.checkPassword(username, password)
        if ok:
            userinfo = UserPro.get_user_by_name(username)
            storage.set("language", userinfo["zone_language"])

            storage.set("tenant_id", userinfo["current_tenant"])
            storage.set("user_id", userinfo["user_id"])
            storage.set("username", username)
        
    if ok:
        return {'message': _('Login successful.')}
    else: 
        raise Exception(_("Invalid username or password"))


@bp.route('/logout', methods=['GET'])
@json_response
def logout():
    _ = getI18n("controllers")
    language = LANGUAGE
    if storage.get("language"):
        language = storage.get("language")
    storage.clearup()
    storage.set("language", language)
    return {'message': _('Logout successful.')}

@bp.route('/change_language', methods=['GET'])
@json_response
def change_language():
    _ = getI18n("controllers")
    if not storage.get("language"):
        storage.set("language", LANGUAGE)
        
    if storage.get("language") == "zh":
        storage.set("language", "en")
    else:
        storage.set("language", "zh")

    if GRADE != "base" and storage.get("username"):
        username = storage.get("username")
        userinfo = UserPro.get_user_by_name(username)
        UserPro.update_user(userinfo["user_id"], zone_language=storage.get("language"))

    return {'message': _('success.')}

@bp.route('/changepassword', methods=['POST'])
@json_response
def changepassword():
    _ = getI18n("controllers")
    data = request.json
    password = data['password']
    phone = data['phone']
    launch_code = data['launch_code']

    UserPro.change_password(phone, password, launch_code)

    return {'message': _('success.')}


@bp.route('/language', methods=['GET'])
@json_response
def language():
    if not storage.get("language"):
        storage.set("language", LANGUAGE)
    
    frontendText = getFrontendText() 

    return {"frontend_text": frontendText}

@bp.route('/send_launch_code', methods=['POST'])
@json_response
def send_launch_code():
    _ = getI18n("frontend")
    data = request.json
    phone = data['phone']
    code_type = data['code_type']

    if len(phone) < 9:
        raise Exception(_("The phone_number cannot be smaller than 9 characters."))
    
    return gen_launch_code(phone, code_type)
