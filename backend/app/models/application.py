from app.extensions import db
from app.models.application_service import ApplicationService

class Application(db.Model):
    app_id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, nullable=False)
    creater = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    default_source_branch = db.Column(db.String(255))
    default_target_branch = db.Column(db.String(255))

    def create(tenant_id, creater, name, description, default_source_branch, default_target_branch):
        if not tenant_id:
            tenant_id = 0

        app = Application(
            tenant_id=tenant_id,
            creater=creater,
            name=name,
            description=description,
            default_source_branch=default_source_branch,
            default_target_branch=default_target_branch
        )
        db.session.add(app)
        db.session.commit()
        return app

    @staticmethod
    def get_all_application(owner, appID):
        applications = Application.query.all()
        if appID:
            applications = Application.query.filter_by(app_id=appID).all()

        application_list = []
        
        for app in applications:
            app_dict = {
                'app_id': app.app_id,
                'tenant_id': app.tenant_id,
                'creater': app.creater,
                'name': app.name,
                'description': app.description,
                'default_source_branch': app.default_source_branch,
                'default_target_branch': app.default_target_branch,
                'service': ApplicationService.get_services_by_app_id(app.app_id)
            }
            application_list.append(app_dict)
        
        return application_list
