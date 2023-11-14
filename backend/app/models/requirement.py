from datetime import datetime
from app.extensions import db
from app.models.application import Application

class Requirement(db.Model):
    requirement_id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, nullable=False)
    requirement_name = db.Column(db.String(6000), nullable=False)
    original_requirement = db.Column(db.String(6000))
    app_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(100))
    default_source_branch = db.Column(db.String(255))
    default_target_branch = db.Column(db.String(255))
    status = db.Column(db.String(20))
    satisfaction_rating = db.Column(db.Integer)
    completion_rating = db.Column(db.Integer)
    created_at = db.Column(db.String(100), default=db.func.current_timestamp())
    updated_at = db.Column(db.String(100), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    @staticmethod
    def create_requirement(tenant_id, requirement_name, original_requirement, app_id, username, default_source_branch, default_target_branch, status, satisfaction_rating=None, completion_rating=None):
        requirement = Requirement(
            tenant_id=tenant_id,
            requirement_name=requirement_name,
            original_requirement=original_requirement,
            app_id=app_id,
            username=username,
            status=status,
            default_source_branch=default_source_branch,
            default_target_branch=default_target_branch,
            satisfaction_rating=satisfaction_rating,
            completion_rating=completion_rating
        )
        db.session.add(requirement)
        db.session.commit()
        return requirement

    @staticmethod
    def get_all_requirements(tenantID=None, page=1, per_page=40):
        requirements = Requirement.query.filter_by(tenant_id=tenantID).order_by(Requirement.requirement_id.desc()).paginate(page=page, per_page=per_page, error_out=False)
        requirement_list = []

        for req in requirements.items:
            req_dict = {
                'requirement_id': req.requirement_id,
                'requirement_name': req.requirement_name,
                'original_requirement': req.original_requirement,
                'app_id': req.app_id,
                'username': req.username,
                'default_source_branch': req.default_source_branch,
                'default_target_branch': req.default_target_branch,
                'status': req.status,
                'satisfaction_rating': req.satisfaction_rating,
                'completion_rating': req.completion_rating,
                'created_at': req.created_at,
                'updated_at': req.updated_at
            }
            requirement_list.append(req_dict)

        return {
            'requirements': requirement_list,
            'total_pages': requirements.pages,
            'current_page': requirements.page,
            'total_items': requirements.total
        }

    @staticmethod
    def get_requirement_by_id(requirement_id, tenant_id=0):
        tenant_id = int(tenant_id)
        req = Requirement.query.get(requirement_id)
        if req:
            req_dict = {
                    'requirement_id': req.requirement_id,
                    'requirement_name': req.requirement_name,
                    'original_requirement': req.original_requirement,
                    'app_id': req.app_id,
                    'tenant_id': req.tenant_id,
                    'username': req.username,
                    'default_source_branch': req.default_source_branch,
                    'default_target_branch': req.default_target_branch,
                    'status': req.status,
                    'satisfaction_rating': req.satisfaction_rating,
                    'completion_rating': req.completion_rating,
                    'created_at': str(req.created_at),
                    'updated_at': str(req.updated_at),
                    'app': Application.get_application_by_id(req.app_id)
                }
            if tenant_id and tenant_id != req_dict["tenant_id"]:
                return None
            return req_dict
        return None

    @staticmethod
    def update_requirement(requirement_id, tenant_id, **kwargs):
        tenant_id = int(tenant_id)
        requirement = Requirement.query.get(requirement_id)
        if not requirement:
            print("update_requirement requirement not found:"+requirement_id)
            return None
        
        if tenant_id and tenant_id != requirement.tenant_id:
            return None
        
        if requirement:
            for key, value in kwargs.items():
                setattr(requirement, key, value)
            requirement.updated_at = datetime.utcnow()
            db.session.commit()
            return requirement
        return None

    @staticmethod
    def delete_requirement(requirement_id, tenant_id):
        tenant_id = int(tenant_id)
        requirement = Requirement.query.get(requirement_id)
        if tenant_id and tenant_id != requirement.tenant_id:
            return None
        if requirement:
            db.session.delete(requirement)
            db.session.commit()
            return True
        return False
