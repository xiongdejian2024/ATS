"""在独立临时MySQL库验证个人视图增量升级与组合筛选，不执行台架。"""

import importlib.util
import json
import logging
from pathlib import Path
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
logging.basicConfig(
    filename=ROOT / "logs/case-views-mysql.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("个人视图数据库验收")


def main():
    import pymysql
    from sqlalchemy import create_engine, text, inspect
    from sqlalchemy.engine import URL
    from sqlalchemy.orm import sessionmaker
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from api.deps import get_current_user
    from api.v1.case_governance import router
    from database import Base, get_db
    import models
    from models import User, Project, TestCase
    from models.case_governance import CaseSavedView, CaseVersion
    from models.task_queue import TaskQueue
    from services.case_query import query_cases

    def root_sql(sql):
        return subprocess.run(
            [
                "docker",
                "exec",
                "-i",
                "ats-mysql",
                "sh",
                "-c",
                'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" exec mysql --user=root --batch --skip-column-names',
            ],
            input=sql,
            text=True,
            capture_output=True,
            timeout=15,
            check=True,
        ).stdout.strip()

    config = json.loads(subprocess.check_output(["docker", "inspect", "ats-mysql"]))[0]
    env = dict(v.split("=", 1) for v in config["Config"]["Env"] if "=" in v)
    connection = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user=env["MYSQL_USER"],
        password=env["MYSQL_PASSWORD"],
        database=env["MYSQL_DATABASE"],
    )
    with connection.cursor() as cursor:
        cursor.execute("SELECT CURRENT_USER()")
        account, host = cursor.fetchone()[0].rsplit("@", 1)
    connection.close()
    name = "ats_case_views_" + uuid.uuid4().hex[:16]
    quote = lambda value: "'" + pymysql.converters.escape_string(value) + "'"
    created = granted = False
    engine = None
    try:
        root_sql(f"CREATE DATABASE `{name}` CHARACTER SET utf8mb4")
        created = True
        root_sql(
            f"GRANT ALL PRIVILEGES ON `{name}`.* TO {quote(account)}@{quote(host)}"
        )
        granted = True
        engine = create_engine(
            URL.create(
                "mysql+pymysql",
                username=env["MYSQL_USER"],
                password=env["MYSQL_PASSWORD"],
                host="127.0.0.1",
                port=3306,
                database=name,
            )
        )
        Base.metadata.create_all(engine)
        Sessions = sessionmaker(bind=engine)
        with engine.begin() as conn:
            conn.execute(
                text(
                    "ALTER TABLE case_saved_views MODIFY COLUMN name VARCHAR(100) NOT NULL"
                )
            )
        with Sessions() as db:
            owner = User(
                id="view-owner",
                username="视图验收",
                email="view@example.test",
                password_hash="不登录",
            )
            db.add(owner)
            db.flush()
            db.add(
                Project(
                    id="view-project",
                    name="独立视图项目",
                    owner_id=owner.id,
                    created_by=owner.id,
                )
            )
            db.flush()
            db.add(
                CaseSavedView(
                    id="old-view",
                    project_id="view-project",
                    owner_id=owner.id,
                    name="历史名称",
                    filters={"search": "中文历史条件"},
                )
            )
            for i in range(3):
                db.add(
                    TestCase(
                        id=f"view-case-{i}",
                        case_code=f"VIEW-{i}",
                        project_id="view-project",
                        name=f"组合用例{i}",
                        type="functional",
                        created_by=owner.id,
                        tags=["冒烟"] if i == 1 else [],
                        steps=[],
                        is_automated=False,
                    )
                )
            db.commit()
        spec = importlib.util.spec_from_file_location(
            "视图增量升级", ROOT / "scripts/upgrade_ms_workspace.py"
        )
        migration = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(migration)
        preview = migration.upgrade(engine, False)
        assert len(preview) == 1 and "个人视图" in preview[0][0], preview
        migration.upgrade(engine, True)
        assert migration.upgrade(engine, False) == []
        with Sessions() as db:
            assert db.get(CaseSavedView, "old-view").filters == {
                "search": "中文历史条件"
            }
            user = db.get(User, "view-owner")
            app = FastAPI()
            app.include_router(router, prefix="/api/v1")
            app.dependency_overrides[get_db] = lambda: db
            app.dependency_overrides[get_current_user] = lambda: user
            path = "/api/v1/projects/view-project/case-governance/views"
            with TestClient(app) as client:
                filters = {
                    "filterLogic": "or",
                    "filterConditions": [
                        {"field": "tags", "operator": "count_gt", "value": 0}
                    ],
                }
                updated = client.put(
                    path + "/old-view", json={"name": "名" * 255, "filters": filters}
                )
                assert updated.status_code == 200, updated.text
                assert updated.json()["data"]["id"] == "old-view"
                copied = client.post(
                    path, json={"name": "另存视图", "filters": filters}
                )
                assert copied.status_code == 200, copied.text
                assert copied.json()["data"]["id"] != "old-view"
                conflict = client.put(
                    path + "/old-view", json={"name": "另存视图", "filters": {}}
                )
                assert conflict.status_code == 409, conflict.text
                assert db.get(CaseSavedView, "old-view").filters == filters
                for i in range(8):
                    assert (
                        client.post(
                            path, json={"name": f"视图{i}", "filters": {}}
                        ).status_code
                        == 200
                    )
                assert (
                    client.post(
                        path, json={"name": "第11个", "filters": {}}
                    ).status_code
                    == 409
                )
            selected = query_cases(
                db,
                "view-project",
                filters={
                    "logic": "or",
                    "conditions": [
                        {"field": "name", "operator": "contains", "value": ""},
                        {"field": "tags", "operator": "count_gt", "value": 0},
                    ],
                },
            )
            assert selected["total"] == 1 and selected["items"][0].id == "view-case-1"
            assert db.query(CaseVersion).count() == db.query(TaskQueue).count() == 0
            lengths = {
                c["name"]: c["type"]
                for c in inspect(engine).get_columns("case_saved_views")
            }
            assert lengths["name"].length == 255
        log.info(
            "真实MySQL验收通过：历史筛选保留、255字符、同ID更新、独立副本、重名回滚、10个上限、OR空值忽略，0用例版本/0节点任务"
        )
        print("真实MySQL个人视图与筛选验收通过")
    except Exception:
        log.exception("真实MySQL个人视图验收失败")
        raise
    finally:
        if engine is not None:
            engine.dispose()
        if granted:
            root_sql(
                f"REVOKE ALL PRIVILEGES ON `{name}`.* FROM {quote(account)}@{quote(host)}"
            )
        if created:
            root_sql(f"DROP DATABASE `{name}`")
        log.info("独立临时库与临时授权已回收：%s", name)


if __name__ == "__main__":
    main()
