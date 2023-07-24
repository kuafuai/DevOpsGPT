from flask import request, session
from app.controllers.common import json_response
from flask import Blueprint
from app.models.app import App
from app.extensions import db
from app.models.app_pro import AppPro
from app.pkgs.tools.i18b import getI18n
from config import GRADE

bp = Blueprint('app', __name__, url_prefix='/app')


@bp.route('/add', methods=['POST'])
@json_response
def add():
    _ = getI18n("controllers")
    name = request.json.get('name')
    intro = request.json.get('intro')
    default_source_branch = request.json.get('default_source_branch')
    default_target_branch = request.json.get('default_target_branch')
    api_doc_url = request.json.get('api_doc_url')
    owner = session['username']

    app = App(owner=owner, name=name, default_source_branch=default_source_branch,
              intro=intro, default_target_branch=default_target_branch, api_doc_url=api_doc_url)

    try:
        db.session.add(app)
        db.session.commit()
        return {'success': True}
    except Exception as e:
        raise Exception(_("Failed to add an application."))


@bp.route('/get', methods=['GET'])
@json_response
def getAll():
    _ = getI18n("controllers")
    owner = session['username']

    try:
        if GRADE == "base":
            apps = App.getAll(owner)
        else:
            apps = AppPro.getAll(owner)

        return {'apps': apps}
    except Exception as e:
        raise Exception(_("Failed to get applications.")) 
