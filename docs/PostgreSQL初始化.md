# PostgreSQL 专用 schema 初始化

`scripts/init_postgres.py` 为原版 ATS 后端创建现有 SQLAlchemy 模型表，当前共 82 张。
它不是 MySQL 数据搬迁器，也不会升级既有表结构。

为 ATS 使用专用且不对 Supabase Data API 暴露的 schema，默认 `ats`。运行时设置
`DATABASE_SCHEMA=ats`，并通过后端的 `DATABASE_URL` 配置 PostgreSQL 连接。连接信息
仅留在服务端环境中；不要把密码写在命令行、前端配置或日志里。

```bash
# 默认仅只读预检，输出将创建的 schema/表；不写入任何数据。
python scripts/init_postgres.py --schema ats

# 审核计划后显式执行；一次事务内创建 schema 和缺失的表。
python scripts/init_postgres.py --schema ats --apply

# 再次预检应显示 createSchema=false、createTables=[]。
python scripts/init_postgres.py --schema ats
```

未给出 `--schema` 时使用 `DATABASE_SCHEMA`，该变量为空时默认 `ats`。命令会在导入
后端连接配置之前为自身进程设置目标 schema；它不改变调用者的环境变量。运行服务时
仍须显式设置同一个 `DATABASE_SCHEMA`，不能依靠 PostgreSQL 的默认 `public`。

`--schema` 只接受最多 63 字符、以小写字母开头的小写字母/数字/下划线标识符。
`public`、`auth`、`storage`、`pg_*`、`information_schema` 及已知 Supabase 管理 schema
均被拒绝。脚本只检查所选 schema，不为公开角色授权、不改 RLS、也不读业务行。
数据库账号需要连接和目录读取权限；执行新建还需要相应数据库/schema 的创建权限。

已有 ATS 表会在任何创建动作之前校验列名、类型、可空性、服务端默认值、主键、
外键（包括目标 schema 和删除行为）、唯一约束、必要索引与检查约束。未知表/视图、
缺失约束、额外列、额外唯一索引等结构差异会直接拒绝执行。额外普通索引可以保留。
已有表不做 ALTER、DROP、重建、数据覆盖或静默修复；结构差异需要另行准备、审核迁移。

应用过程以事务级锁防止该工具同时初始化同一 schema，并锁住既有 ATS 表以防预检期间
被其他 DDL 改变。创建后重新反射校验，任何失败都会回滚本次事务。锁等待上限 10 秒。
仍应在维护窗口执行，避免其他工具同时变更 schema。失败输出不会打印数据库驱动的
原始错误，以免泄露连接信息。

单元测试验证默认只读、结构漂移拒绝、受保护 schema 拒绝与事务控制；实际 PostgreSQL
集成测试还必须验证新建、幂等、保留既有数据及失败回滚。初始化成功不代表数据迁移、
完整业务验收或生产部署完成。
