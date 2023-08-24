"""create_requirement_memory

Revision ID: 9fcba96eac25
Revises: 652cd7f16123
Create Date: 2023-08-23 14:23:11.425971

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9fcba96eac25'
down_revision = '652cd7f16123'
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
        CREATE TABLE requirement_memory (
        memory_id '''+primaryKeyAdditional+''',
        requirement_id '''+intAdditional+''', -- 关联需求的需求ID
        input_content TEXT, -- 输入内容
        output_content TEXT, -- 返回内容
        visibility char(20), -- 前端可见性：Visible、Hidden
        step char(20), -- 步骤:'requirement', 'api', 'subtask', 'code', 'ci', 'cd'
        artifact_type char(30), -- 制品类型:'RequirementDocument', 'InterfaceDocument', 'Pseudocode', 'Code', 'Image', 'DeploymentAddress'
        artifact_path VARCHAR(255), -- 制品路径
        artifact_content TEXT, -- 制品内容
        satisfaction_rating '''+intAdditional+''', -- 满意度评分，可以为空
        completion_rating '''+intAdditional+''', -- 完成度评分，可以为空
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) '''+additional+''';
    ''')


def downgrade() -> None:
    op.execute('DROP TABLE IF EXISTS requirement_memory')
