from app.extensions import db
from app.models.application_service_lib import ApplicationServiceLib

class ApplicationService(db.Model):
    service_id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.Integer, db.ForeignKey('application.app_id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    git_path = db.Column(db.String(255))
    git_workflow = db.Column(db.String(255))
    role = db.Column(db.Text)
    language = db.Column(db.String(50))
    framework = db.Column(db.String(50))
    database = db.Column(db.String(50))
    api_type = db.Column(db.String(50))
    api_location = db.Column(db.String(255))
    struct_cache = db.Column(db.Text)
    cd_container_name = db.Column(db.String(100))
    cd_container_group = db.Column(db.String(100))
    cd_region = db.Column(db.String(100))
    cd_public_ip = db.Column(db.String(50))
    cd_security_group = db.Column(db.String(100))
    cd_subnet = db.Column(db.String(100))
    created_at = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP'))
    updated_at = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP'))

    def create_service(app_id, name, git_path, git_workflow, role, language, framework, database, api_type, api_location,
                       cd_container_name, cd_container_group, cd_region, cd_public_ip, cd_security_group, cd_subnet, struct_cache):
        service = ApplicationService(
            app_id=app_id,
            name=name,
            git_path=git_path,
            git_workflow=git_workflow,
            role=role,
            language=language,
            framework=framework,
            database=database,
            api_type=api_type,
            api_location=api_location,
            cd_container_name=cd_container_name,
            cd_container_group=cd_container_group,
            cd_region=cd_region,
            cd_public_ip=cd_public_ip,
            cd_security_group=cd_security_group,
            cd_subnet=cd_subnet,
            struct_cache=struct_cache
        )
        db.session.add(service)
        db.session.commit()
        return service

    @classmethod
    def get_all_services(cls):
        return cls.query.all()

    @classmethod
    def get_service_by_id(cls, service_id):
        return cls.query.get(service_id)
    
    @staticmethod
    def get_service_by_name(appID, service_name):
        services = ApplicationService.query.filter_by(name=service_name, app_id=appID).all()
        print("########")
        print(appID)
        print(service_name)
        print(services)

        service_dict = {}
        for service in services:
            service_dict = {
                'service_id': service.service_id,
                'app_id': service.app_id,
                'name': service.name,
                'git_path': service.git_path,
                'git_workflow': service.git_workflow,
                'role': service.role,
                'language': service.language,
                'framework': service.framework,
                'database': service.database,
                'api_type': service.api_type,
                'api_location': service.api_location,
                'cd_container_name': service.cd_container_name,
                'cd_container_group': service.cd_container_group,
                'cd_region': service.cd_region,
                'cd_public_ip': service.cd_public_ip,
                'cd_security_group': service.cd_security_group,
                'cd_subnet': service.cd_subnet,
                'struct_cache': service.struct_cache,
                'libs': ApplicationServiceLib.get_libs_by_service_id(service.service_id)
            }

        return service_dict

    def update_service(self, name, git_path, git_workflow, role, language, framework, database, api_type, api_location):
        self.name = name
        self.git_path = git_path
        self.git_workflow = git_workflow
        self.role = role
        self.language = language
        self.framework = framework
        self.database = database
        self.api_type = api_type
        self.api_location = api_location
        db.session.commit()

    @classmethod
    def delete_service(cls, service_id):
        service = cls.query.get(service_id)
        if service:
            db.session.delete(service)
            db.session.commit()
            return True
        return False

    @classmethod
    def get_services_by_app_id(cls, app_id):
        services = cls.query.filter_by(app_id=app_id).all()
        services_list = []
        
        for service in services:
            service_dict = {
                'service_id': service.service_id,
                'app_id': service.app_id,
                'name': service.name,
                'git_path': service.git_path,
                'git_workflow': service.git_workflow,
                'role': service.role,
                'language': service.language,
                'framework': service.framework,
                'database': service.database,
                'api_type': service.api_type,
                'api_location': service.api_location,
                'cd_container_name': service.cd_container_name,
                'cd_container_group': service.cd_container_group,
                'cd_region': service.cd_region,
                'cd_public_ip': service.cd_public_ip,
                'cd_security_group': service.cd_security_group,
                'cd_subnet': service.cd_subnet,
                'struct_cache': service.struct_cache,
                'libs': ApplicationServiceLib.get_libs_by_service_id(service.service_id)
            }
            services_list.append(service_dict)
        
        return services_list
