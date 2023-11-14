from .user import bp as user_bp
from .requirement import bp as requirement_bp
from .workspace import bp as workspace_bp
from .app import bp as app_bp
from .step_devops import bp as step_devops_bp
from .step_subtask import bp as step_subtask_bp
from .step_code import bp as step_code_bp
from .step_api import bp as step_api_bp
from .step_requirement import bp as step_requirement_bp
from .setting import bp as setting_bp
from .tenant_pro import bp as tenant_bp
from .pay_pro import bp as pay_bp
from .plugine_api import bp as plugine_bp
from .tencent_pro import bp as tencent_bp

def register_controllers(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(requirement_bp)
    app.register_blueprint(workspace_bp)
    app.register_blueprint(app_bp)
    app.register_blueprint(step_requirement_bp)
    app.register_blueprint(step_api_bp)
    app.register_blueprint(step_subtask_bp)
    app.register_blueprint(step_code_bp)
    app.register_blueprint(step_devops_bp)
    app.register_blueprint(setting_bp)
    app.register_blueprint(tenant_bp)
    app.register_blueprint(pay_bp)
    app.register_blueprint(plugine_bp)
    app.register_blueprint(tencent_bp)