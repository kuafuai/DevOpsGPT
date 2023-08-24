"""create_application_service

Revision ID: 893be497b93f
Revises: 91bd1a8a419e
Create Date: 2023-08-23 14:33:58.505851

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '893be497b93f'
down_revision = '91bd1a8a419e'
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
        CREATE TABLE application_service (
            service_id '''+primaryKeyAdditional+''',
            app_id '''+intAdditional+''', -- 关联应用的应用ID
            name VARCHAR(255), -- 服务名称
            git_config_id '''+intAdditional+''', -- 关联的Git配置
            ci_config_id '''+intAdditional+''', -- 关联的CI配置
            cd_config_id '''+intAdditional+''', -- 关联的CD配置
            cd_container_name VARCHAR(100), -- 容器名称
            cd_container_group VARCHAR(100), -- 容器组名称
            cd_region VARCHAR(100), -- 区域
            cd_public_ip VARCHAR(50), -- 公网IP
            cd_security_group VARCHAR(100), -- 安全组
            cd_subnet VARCHAR(100), -- 交换机
            git_path VARCHAR(100), -- Git仓库路径
            git_workflow VARCHAR(100), -- Git工作流
            role VARCHAR(500), -- 服务用途
            struct_cache TEXT, -- 应用结构缓存
            language VARCHAR(50), -- 编程语言
            framework VARCHAR(100), -- 框架
            database VARCHAR(50), -- 数据库
            api_type VARCHAR(50), -- API类型
            api_location TEXT, -- API位置
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) '''+additional+''';
    ''')

def downgrade():
    # 使用原生SQL删除表格
    op.execute('DROP TABLE IF EXISTS application_service')
