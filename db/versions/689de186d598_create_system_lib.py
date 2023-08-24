"""create_system_lib

Revision ID: 689de186d598
Revises: 06799343c2ab
Create Date: 2023-08-23 14:34:44.617393

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '689de186d598'
down_revision = '06799343c2ab'
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
        CREATE TABLE sys_lib (
            sys_lib_id '''+primaryKeyAdditional+''',
            lib_name VARCHAR(255), -- 库名称
            purpose VARCHAR(255), -- 用途
            specification VARCHAR(255), -- 规范
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) '''+additional+''';
    ''')

def downgrade():
    # 使用原生SQL删除表格
    op.execute('DROP TABLE IF EXISTS sys_lib')
