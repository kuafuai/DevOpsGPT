服务的文件目录说明:
dir:src/main/java/com/aiassistant/web/controller,description:页面对外服务接口
dir:src/main/java/com/aiassistant/service,description:业务层Service接口定义
dir:src/main/java/com/aiassistant/service/mapper,description:与数据库交互的Mapper
dir:src/main/java/com/aiassistant/service/impl,description:业务层Service接口具体实现
dir:src/main/java/com/aiassistant/config,description:服务config配置
dir:src/main/java/com/aiassistant/model,description:数据库字段映射实体类
dir:src/main/resources,description:服务资源配置
dir:src/main/resources/mapper,description:数据库操作的sql
dir:src/main/resources/mybatis,description:数据库mybatis配置
dir:src/main/resources/db/migration,description:数据库版本控制脚本
file:src/main/resources/application.yml,description:服务参数配置
file:src/main/resources/application-druid.yml,description:服务数据库参数配置

增加flyway的使用文档，保留原有的内容：

1. 在pom.xml中添加以下依赖：