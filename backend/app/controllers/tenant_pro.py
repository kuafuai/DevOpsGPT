from flask import Blueprint
from app.controllers.common import json_response
from app.pkgs.tools.i18b import getI18n

bp = Blueprint('tenant', __name__, url_prefix='/tenant')

def test():
    pass

@bp.route('/get_all', methods=['GET'])
@json_response
def get_all():
    _ = getI18n("controllers")
    raise Exception(_("The current version does not support this feature."))

@bp.route('/create', methods=['POST'])
@json_response
def create():
    _ = getI18n("controllers")
    raise Exception(_("The current version does not support this feature."))