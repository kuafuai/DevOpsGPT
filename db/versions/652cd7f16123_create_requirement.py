"""create_requirement

Revision ID: 652cd7f16123
Revises: 
Create Date: 2023-08-23 14:22:35.525896

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '652cd7f16123'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    engine_name = conn.dialect.name
    additional = "ENGINE=InnoDB DEFAULT CHARSET=utf8"
    primaryKeyAdditional = "INT AUTO_INCREMENT PRIMARY KEY"
    intAdditional = "INT DEFAULT 0"
    if engine_name == 'sqlite':
        additional = ""
        primaryKeyAdditional = "INTEGER PRIMARY KEY AUTOINCREMENT"
        intAdditional = "INTEGER DEFAULT 0"

    op.execute('''
        CREATE TABLE requirement (
        requirement_id '''+primaryKeyAdditional+''',
        requirement_name VARCHAR(255), -- 需求名称
        original_requirement VARCHAR(1000), -- 原始需求描述
        app_id '''+intAdditional+''', -- 关联应用的应用ID
        user_id '''+intAdditional+''', -- 创建用户的用户ID
        status char(20), -- 需求状态 'Open', 'InProgress', 'Completed', 'Canceled'
        satisfaction_rating '''+intAdditional+''', -- 满意度评分，可以为空
        completion_rating '''+intAdditional+''', -- 完成度评分，可以为空
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) '''+additional+''' ;
    ''')


def downgrade() -> None:
    op.execute('DROP TABLE IF EXISTS requirement')
