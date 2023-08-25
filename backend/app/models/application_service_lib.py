from app.extensions import db

class ApplicationServiceLib(db.Model):
    lib_id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('application_service.service_id'), nullable=False)
    sys_lib_name = db.Column(db.String(200))
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def create_libs(service_id, libs_name):
        import re
        separator_pattern = r'[,，]'
        libs_array = re.split(separator_pattern, libs_name)

        # 遍历数组中的元素
        libs = []
        for sys_lib_name in libs_array:
            libs.append(ApplicationServiceLib.create_lib(service_id, sys_lib_name))
        return libs

    # 创建Lib
    def create_lib(service_id, sys_lib_name):
        lib = ApplicationServiceLib(
            service_id=service_id,
            sys_lib_name=sys_lib_name
        )
        db.session.add(lib)
        db.session.commit()
        return lib

    # 查询所有Lib
    def get_all_libs():
        return ApplicationServiceLib.query.all()

    # 根据lib_id查询Lib
    def get_lib_by_id(lib_id):
        return ApplicationServiceLib.query.get(lib_id)

    # 更新Lib信息
    def update_lib(lib_id, sys_lib_name):
        lib = ApplicationServiceLib.query.get(lib_id)
        if lib:
            lib.sys_lib_name = sys_lib_name
            db.session.commit()
            return lib
        return None

    # 删除Lib
    def delete_lib(lib_id):
        lib = ApplicationServiceLib.query.get(lib_id)
        if lib:
            db.session.delete(lib)
            db.session.commit()
            return True
        return False

    def get_libs_by_service_id(service_id):
        libs = ApplicationServiceLib.query.filter_by(service_id=service_id).all()
        libs_list = []
        
        for lib in libs:
            lib_dict = {
                'lib_id': lib.lib_id,
                'service_id': lib.service_id,
                'sys_lib_name': lib.sys_lib_name
            }
            libs_list.append(lib_dict)
        
        return libs_list
