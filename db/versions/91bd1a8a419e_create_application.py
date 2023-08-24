"""create_application

Revision ID: 91bd1a8a419e
Revises: 9fcba96eac25
Create Date: 2023-08-23 14:33:31.231262

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91bd1a8a419e'
down_revision = '9fcba96eac25'
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
        CREATE TABLE application (
            app_id '''+primaryKeyAdditional+''',
            tenant_id '''+intAdditional+''', -- 关联租户的租户ID
            creater VARCHAR(255), -- 创建者
            name VARCHAR(255), -- 应用名称
            description VARCHAR(255), -- 应用描述
            default_source_branch VARCHAR(255), -- 默认源分支
            default_target_branch VARCHAR(255), -- 默认目标分支
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) '''+additional+''';
    ''')

def downgrade():
    # 使用原生SQL删除表格
    op.execute('DROP TABLE IF EXISTS application')
