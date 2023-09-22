from sqlalchemy import func
from app.extensions import db

class SysLib(db.Model):
    sys_lib_id = db.Column(db.Integer, primary_key=True)
    lib_name = db.Column(db.String(255))
    purpose = db.Column(db.String(255))
    specification = db.Column(db.String(255))
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    @staticmethod
    def create_lib(lib_name, purpose, specification):
        sys_lib = SysLib(
            lib_name=lib_name,
            purpose=purpose,
            specification=specification
        )
        db.session.add(sys_lib)
        db.session.commit()
        return sys_lib

    @staticmethod
    def get_all_libs():
        libs = SysLib.query.all()
        lib_list = []
        
        for lib in libs:
            lib_dict = {
                'sys_lib_id': lib.sys_lib_id,
                'lib_name': lib.lib_name,
                'purpose': lib.purpose,
                'specification': lib.specification,
                'created_at': lib.created_at,
                'updated_at': lib.updated_at
            }
            lib_list.append(lib_dict)
        
        return lib_list

    @staticmethod
    def get_lib_by_name(sys_lib_name):
        sys_lib_name = sys_lib_name.lower()

        libs = SysLib.query.filter(func.lower(SysLib.lib_name).ilike(sys_lib_name)).all()

        lib_dict = {}
        for lib in libs:
            lib_dict = {
                'sys_lib_id': lib.sys_lib_id,
                'lib_name': lib.lib_name,
                'purpose': lib.purpose,
                'specification': lib.specification,
                'created_at': lib.created_at,
                'updated_at': lib.updated_at
            }

        return lib_dict

    @staticmethod
    def update_lib(sys_lib_id, lib_name, purpose, specification):
        sys_lib = SysLib.query.get(sys_lib_id)
        if sys_lib:
            sys_lib.lib_name = lib_name
            sys_lib.purpose = purpose
            sys_lib.specification = specification
            db.session.commit()
            return sys_lib
        return None

    @staticmethod
    def delete_lib(sys_lib_id):
        sys_lib = SysLib.query.get(sys_lib_id)
        if sys_lib:
            db.session.delete(sys_lib)
            db.session.commit()
            return True
        return False
