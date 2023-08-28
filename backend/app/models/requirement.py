from app.extensions import db
from app.models.application import Application

class Requirement(db.Model):
    requirement_id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, nullable=False)
    requirement_name = db.Column(db.String(255), nullable=False)
    original_requirement = db.Column(db.String(1000))
    app_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    default_source_branch = db.Column(db.String(255))
    default_target_branch = db.Column(db.String(255))
    status = db.Column(db.String(20))
    satisfaction_rating = db.Column(db.Integer)
    completion_rating = db.Column(db.Integer)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    @staticmethod
    def create_requirement(tenant_id, requirement_name, original_requirement, app_id, user_id, default_source_branch, default_target_branch, status, satisfaction_rating=None, completion_rating=None):
        requirement = Requirement(
            tenant_id=tenant_id,
            requirement_name=requirement_name,
            original_requirement=original_requirement,
            app_id=app_id,
            user_id=user_id,
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
    def get_all_requirements(tenantID=None):
        requirements = Requirement.query.filter_by(tenant_id=tenantID).order_by(Requirement.requirement_id.desc()).all()
        requirement_list = []

        for req in requirements:
            req_dict = {
                'requirement_id': req.requirement_id,
                'requirement_name': req.requirement_name,
                'original_requirement': req.original_requirement,
                'app_id': req.app_id,
                'user_id': req.user_id,
                'default_source_branch': req.default_source_branch,
                'default_target_branch': req.default_target_branch,
                'status': req.status,
                'satisfaction_rating': req.satisfaction_rating,
                'completion_rating': req.completion_rating,
                'created_at': req.created_at,
                'updated_at': req.updated_at
            }
            requirement_list.append(req_dict)

        return requirement_list

    @staticmethod
    def get_requirement_by_id(requirement_id):
        req = Requirement.query.get(requirement_id)
        req_dict = {
                'requirement_id': req.requirement_id,
                'requirement_name': req.requirement_name,
                'original_requirement': req.original_requirement,
                'app_id': req.app_id,
                'user_id': req.user_id,
                'default_source_branch': req.default_source_branch,
                'default_target_branch': req.default_target_branch,
                'status': req.status,
                'satisfaction_rating': req.satisfaction_rating,
                'completion_rating': req.completion_rating,
                'created_at': req.created_at,
                'updated_at': req.updated_at,
                'app': Application.get_application_by_id(req.app_id)
            }
        return req_dict

    @staticmethod
    def update_requirement(requirement_id, requirement_name=None, original_requirement=None, app_id=None, user_id=None, status=None, satisfaction_rating=None, completion_rating=None):
        requirement = Requirement.query.get(requirement_id)
        
        if requirement:
            if requirement_name is not None:
                requirement.requirement_name = requirement_name
            if original_requirement is not None:
                requirement.original_requirement = original_requirement
            if app_id is not None:
                requirement.app_id = app_id
            if user_id is not None:
                requirement.user_id = user_id
            if status is not None:
                requirement.status = status
            if satisfaction_rating is not None:
                requirement.satisfaction_rating = satisfaction_rating
            if completion_rating is not None:
                requirement.completion_rating = completion_rating
            
            db.session.commit()
            return requirement
        
        return None


    @staticmethod
    def delete_requirement(requirement_id):
        requirement = Requirement.query.get(requirement_id)
        if requirement:
            db.session.delete(requirement)
            db.session.commit()
            return True
        return False
