"""在独立临时MySQL库验证接口定义迁移、视图隔离及规划关联原子保存，不入队或执行台架。"""

import json
import logging
from pathlib import Path
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
logging.basicConfig(
    filename=ROOT / "logs/第63部分MySQL验收.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("接口双模式数据库验收")


def main(verify_basic=None):
    import pymysql
    from sqlalchemy import create_engine
    from sqlalchemy.engine import URL
    from sqlalchemy.orm import sessionmaker
    from database import Base
    import models
    from models import User, Project, TestCase
    from models.task_queue import TaskQueue

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
    name = ("ats_candidate_" if verify_basic else "ats_definition_") + uuid.uuid4().hex[
        :16
    ]
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
        from fastapi import HTTPException
        from models import TestPlan, PlanCaseRelation
        from models.plan_workspace import PlanNode
        from services.plan_minder_edit import (
            load,
            save,
            MinderSave,
            MinderCandidatePreview,
            preview_candidates,
        )
        from schemas.plan_candidate_selection import CandidateSelection, Association

        with Sessions() as db:
            db.add(
                User(
                    id="owner",
                    username="关联验收",
                    email="draft@example.test",
                    password_hash="不登录",
                )
            )
            db.flush()
            db.add(Project(id="project", name="独立关联项目", owner_id="owner"))
            db.flush()
            db.add(
                TestPlan(
                    id="plan",
                    project_id="project",
                    owner_id="owner",
                    name="关联规划",
                    plan_number="DRAFT",
                )
            )
            db.flush()
            from models import Module
            from models.native_case import ApiDefinition, NativeCaseConfig
            from sqlalchemy import inspect, text
            import importlib.util

            # 临时库模拟历史表，再运行增量迁移；正式库在此脚本中只读连接信息。
            db.commit()
            with engine.begin() as connection:
                for constraint in inspect(connection).get_foreign_keys(
                    "native_api_definitions"
                ):
                    if tuple(constraint["constrained_columns"]) in {
                        ("module_id",),
                        ("created_by",),
                    }:
                        connection.execute(
                            text(
                                "ALTER TABLE native_api_definitions DROP FOREIGN KEY `"
                                + constraint["name"]
                                + "`"
                            )
                        )
                for column in ("module_id", "state", "tags", "created_by"):
                    connection.execute(
                        text("ALTER TABLE native_api_definitions DROP COLUMN " + column)
                    )
            db.commit()
            db.execute(
                text(
                    "INSERT INTO native_api_definitions (id,project_id,name,protocol,path,parameters,revision,updated_by) VALUES ('history','project','历史接口','HTTP','/history','{}',1,'owner')"
                )
            )
            db.commit()
            spec = importlib.util.spec_from_file_location(
                "metadata_migration",
                ROOT / "scripts/upgrade_api_definition_metadata.py",
            )
            migration = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(migration)
            assert migration.upgrade(connection_engine=engine) == list(
                migration.COLUMNS
            )
            migration.upgrade(True, engine)
            assert migration.upgrade(True, engine) == []
            history = db.get(ApiDefinition, "history")
            assert (
                history.name == "历史接口"
                and history.module_id
                is history.state
                is history.tags
                is history.created_by
                is None
            )
            db.add(Module(id="module", project_id="project", name="接口模块"))
            db.flush()
            history.module_id = "module"
            db.add(
                ApiDefinition(
                    id="excluded",
                    project_id="project",
                    name="被排除接口",
                    protocol="HTTP",
                    path="/excluded",
                    parameters={},
                    module_id="module",
                    updated_by="owner",
                )
            )
            db.add(
                ApiDefinition(
                    id="empty",
                    project_id="project",
                    name="空接口",
                    protocol="HTTP",
                    path="/empty",
                    parameters={},
                    updated_by="owner",
                )
            )
            db.flush()
            for i in range(3):
                case = TestCase(
                    id=f"case-{i}",
                    project_id="project",
                    case_code=f"DEF-{i}",
                    name=f"接口子用例{i}",
                    type="api",
                    is_automated=True,
                    steps=[],
                    created_by="owner",
                )
                db.add(case)
                db.flush()
                db.add(
                    NativeCaseConfig(
                        case_id=case.id,
                        api_definition_id="history" if i < 2 else "excluded",
                        state="DONE",
                        parameters={},
                        updated_by="owner",
                    )
                )
            db.commit()
            user = db.get(User, "owner")
            if verify_basic:
                verify_basic(db, user)
            from api.v1.plan_case_workspace import candidate_view_scope
            from services import plan_case_view as views
            from schemas.plan_candidate_view import CandidateViewCreate

            api_scope = candidate_view_scope("api", "API")
            assert (
                len(api_scope)
                <= views.PlanCaseSavedView.__table__.c.category.type.length
            )
            view = views.save(
                db,
                user,
                db.get(TestPlan, "plan"),
                api_scope,
                CandidateViewCreate(
                    name="接口个人视图",
                    filters={
                        "filterConditions": [
                            {"field": "caseTotal", "operator": "gt", "value": 1}
                        ],
                        "filterLogic": "and",
                    },
                ),
            )
            db.commit()
            assert (
                views.scope(db, user, db.get(TestPlan, "plan"), api_scope).count() == 1
            )
            assert (
                views.scope(
                    db,
                    user,
                    db.get(TestPlan, "plan"),
                    candidate_view_scope("api", "CASE"),
                ).count()
                == 0
            )
            db.commit()
            log.info(
                "MySQL接口个人视图真实写入通过，内部分类未超过字段长度且与接口用例视图隔离"
            )
            initial = load(db, user, "plan")
            db.commit()
            identifier = str(uuid.uuid4())
            draft = MinderSave(
                expectedFingerprint=initial["fingerprint"],
                points=[
                    dict(
                        id=identifier,
                        name="接口临时目标",
                        category="api",
                        parentId=None,
                        position=0,
                    )
                ],
            )
            chosen = CandidateSelection(
                category="api",
                resourceType="API",
                moduleMaps={"module": dict(selectAll=True, excludeIds=["excluded"])},
            )
            for _ in range(2):
                result = preview_candidates(
                    db,
                    user,
                    "plan",
                    MinderCandidatePreview(draft=draft, selection=chosen),
                )
                db.commit()
                assert (
                    result["selectedDefinitionCount"] == 1
                    and result["count"] == 2
                    and result["excludedCount"] == 1
                )
                assert (
                    db.query(PlanNode).count()
                    == db.query(PlanCaseRelation).count()
                    == 0
                )
                assert load(db, user, "plan")["fingerprint"] == initial["fingerprint"]
                db.commit()
            draft.associations = [
                Association(**chosen.model_dump(), collectionId=identifier),
                Association(
                    category="api", resourceType="API", definitionIds=["missing"]
                ),
            ]
            try:
                save(db, user, "plan", draft)
            except HTTPException as exc:
                db.rollback()
                log.exception("预期晚期接口404，核验第一批与临时集一起回滚")
                assert exc.status_code == 404
            else:
                raise AssertionError("缺失接口未拒绝")
            assert db.query(PlanNode).count() == db.query(PlanCaseRelation).count() == 0
            draft.associations.pop()
            save(db, user, "plan", draft)
            db.commit()
            assert {r.case_id for r in db.query(PlanCaseRelation)} == {
                "case-0",
                "case-1",
            }
            assert db.query(TestCase).count() == 3 and db.query(TaskQueue).count() == 0
            # 接口模式是引用，关联后不改变主用例与定义总数。
            assert (
                db.query(ApiDefinition).count() == 3
                and db.query(NativeCaseConfig).count() == 3
            )
            log.info(
                "MySQL历史元数据迁移幂等、两次预览回滚、按接口排除、晚期404原子回滚及真实子用例关联通过；3主用例/3定义保持，任务0"
            )
            print(
                "MySQL接口双模式验收通过：历史迁移幂等、预览回滚、接口排除、晚期原子回滚和真实子用例关联，无任务。"
            )

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
    try:
        main()
    except Exception:
        log.exception("规划脑图MySQL验收失败")
        raise
