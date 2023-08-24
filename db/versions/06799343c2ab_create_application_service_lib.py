"""create_application_service_lib

Revision ID: 06799343c2ab
Revises: 893be497b93f
Create Date: 2023-08-23 14:34:02.076078

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06799343c2ab'
down_revision = '893be497b93f'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    engine_name = conn.dialect.name
    additional = "ENGINE=InnoDB DEFAULT CHARSET=utf8"
    primaryKeyAdditional = "INT AUTO_INCREMENT PRIMARY KEY"
    intAdditional = "INT DEFAULT 0"
    if engine_name == 'sqlite':
        additional = ""
        primaryKeyAdditional = "INTEGER PRIMARY KEY AUTOINCREMENT"
        intAdditional = "INTEGER DEFAULT 0"

    # 使用原生SQL创建表格
    op.execute('''
        CREATE TABLE application_service_lib (
            lib_id '''+primaryKeyAdditional+''',
            service_id '''+intAdditional+''', -- 关联服务的服务ID
            sys_lib_name VARCHAR(200), -- 库关联系统lib
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) '''+additional+''';
    ''')

def downgrade():
    # 使用原生SQL删除表格
    op.execute('DROP TABLE IF EXISTS application_service_lib')
