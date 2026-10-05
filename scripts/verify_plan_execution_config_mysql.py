"""在独立临时MySQL库验证原生范围批次的当前读、幂等和并发入队，不执行台架。"""

import json
import logging
from pathlib import Path
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
logging.basicConfig(
    filename=ROOT / "logs/第56部分MySQL验收.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("原生计划实例范围数据库验收")


def main():
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
    name = "ats_native_run_" + uuid.uuid4().hex[:16]
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
        from concurrent.futures import ThreadPoolExecutor
        import threading, time
        from fastapi import HTTPException
        from models import TestPlan, TestSuite, PlanCaseRelation, Environment
        from models.plan_orchestration import PlanRun, PlanRunItem, PlanSettings
        from schemas.plan_native_selection import (
            NativeWorkspaceSelection,
            NativeWorkspaceRun,
        )
        from services.plan_native_selection import preview
        from services.plan_native_run import start
        from services.review_workspace import lock_project

        with Sessions() as db:
            db.add(
                User(
                    id="owner",
                    username="范围执行验收",
                    email="run@example.test",
                    password_hash="不登录",
                )
            )
            db.flush()
            db.add(Project(id="project", name="临时范围执行项目", owner_id="owner"))
            db.flush()
            db.add(
                TestPlan(
                    id="plan",
                    project_id="project",
                    owner_id="owner",
                    name="范围执行",
                    plan_number="RANGE",
                )
            )
            db.flush()
            db.add_all(
                [
                    Environment(id="offline", name="绝不执行", is_online=False),
                    Environment(id="new-env", name="新节点", is_online=False),
                ]
            )
            db.flush()
            for i in range(3):
                db.add(
                    TestCase(
                        id=f"case-{i}",
                        project_id="project",
                        case_code=f"CODE-{i}",
                        name=f"用例{i}",
                        type="api",
                        is_automated=True,
                        priority="P1",
                        steps=[],
                        created_by="owner",
                    )
                )
                db.flush()
                db.add(
                    PlanCaseRelation(
                        id=f"relation-{i}",
                        plan_id="plan",
                        case_id=f"case-{i}",
                        execution_order=i,
                    )
                )
            db.add(
                TestSuite(
                    id="suite",
                    plan_id="plan",
                    name="XAT模板",
                    environment_id="offline",
                    execution_command="xat --mode offline",
                    case_ids=[f"case-{i}" for i in range(3)],
                    created_by="owner",
                )
            )
            db.commit()
        scope = dict(
            category="api",
            selectAll=True,
            excludeIds=["legacy:relation-2:case-2"],
            condition=dict(priority="P1"),
        )

        def request():
            return NativeWorkspaceRun(**scope, requestId=str(uuid.uuid4()))

        for label, expected in [
            ("优先级", 1),
            ("新增用例关联", 3),
            ("当前策略与环境", 2),
            ("活动批次", 0),
        ]:
            ready, proceed = threading.Event(), threading.Event()

            def run_stale():
                with Sessions() as db:
                    assert (
                        preview(
                            db,
                            db.get(TestPlan, "plan"),
                            db.get(User, "owner"),
                            NativeWorkspaceSelection(**scope),
                        )["count"]
                        == 2
                    )
                    ready.set()
                    assert proceed.wait(15)
                    try:
                        run = start(
                            db,
                            db.get(TestPlan, "plan"),
                            db.get(User, "owner"),
                            request(),
                        )
                        assert len(run.case_snapshot) == expected, (
                            label,
                            len(run.case_snapshot),
                        )
                        assert (
                            len({row["associationId"] for row in run.case_snapshot})
                            == expected
                        )
                        assert all(row["id"] != "case-2" for row in run.case_snapshot)
                        if label == "当前策略与环境":
                            assert run.config_snapshot["executionMode"] == "parallel"
                            assert all(
                                i.environment_id == "new-env"
                                for i in db.query(PlanRunItem).filter_by(run_id=run.id)
                            )
                            assert db.query(TaskQueue).count() == 2
                        db.rollback()
                        return expected
                    except HTTPException as error:
                        db.rollback()
                        assert label == "活动批次" and error.status_code == 409
                        return 0

            with ThreadPoolExecutor(max_workers=1) as pool:
                pending = pool.submit(run_stale)
                assert ready.wait(15)
                with Sessions() as holder:
                    lock_project(holder, "project")
                    if label == "优先级":
                        holder.get(TestCase, "case-0").priority = "P2"
                    elif label == "新增用例关联":
                        holder.add(
                            TestCase(
                                id="new-case",
                                project_id="project",
                                case_code="NEW",
                                name="新用例",
                                type="api",
                                is_automated=True,
                                priority="P1",
                                steps=[],
                                created_by="owner",
                            )
                        )
                        holder.flush()
                        holder.add(
                            PlanCaseRelation(
                                id="new-relation",
                                plan_id="plan",
                                case_id="new-case",
                                execution_order=3,
                            )
                        )
                        holder.get(TestSuite, "suite").case_ids = [
                            "case-0",
                            "case-1",
                            "case-2",
                            "new-case",
                        ]
                    elif label == "当前策略与环境":
                        holder.add(
                            PlanSettings(plan_id="plan", execution_mode="parallel")
                        )
                        holder.get(TestSuite, "suite").environment_id = "new-env"
                    else:
                        holder.add(
                            PlanRun(
                                id="active",
                                plan_id="plan",
                                executor_id="owner",
                                plan_name="已有批次",
                                status="queued",
                                config_snapshot=dict(
                                    passThreshold=100,
                                    executionMode="serial",
                                    stopOnFailure=False,
                                    suiteOrder=[],
                                ),
                                case_snapshot=[],
                                manual_results={},
                            )
                        )
                    holder.flush()
                    proceed.set()
                    for _ in range(100):
                        waits = root_sql(
                            "SELECT COUNT(*) FROM performance_schema.data_lock_waits w JOIN performance_schema.data_locks l ON w.REQUESTING_ENGINE_LOCK_ID=l.ENGINE_LOCK_ID WHERE l.OBJECT_SCHEMA='"
                            + name
                            + "'"
                        )
                        if int(waits or 0):
                            break
                        time.sleep(0.05)
                    else:
                        raise AssertionError("未观察到真实项目锁等待")
                    assert not pending.done()
                    holder.commit()
                assert pending.result(timeout=15) == expected
            log.info(
                "%s通过：旧预览2，真实项目锁等待后按最新配置冻结%d实例；任务全部回滚，无执行器",
                label,
                expected,
            )
            with Sessions() as db:
                db.get(TestCase, "case-0").priority = "P1"
                db.get(TestSuite, "suite").case_ids = ["case-0", "case-1", "case-2"]
                db.get(TestSuite, "suite").environment_id = "offline"
                db.query(PlanCaseRelation).filter_by(id="new-relation").delete()
                db.query(TestCase).filter_by(id="new-case").delete()
                db.query(PlanSettings).delete()
                db.query(PlanRun).filter_by(id="active").delete()
                db.commit()
        # 原生请求与请求环境不能来自预览时的旧MySQL快照。
        from models.native_case import (
            ApiDefinition,
            ApiTestEnvironment,
            NativeCaseConfig,
        )

        with Sessions() as db:
            db.add(
                ApiDefinition(
                    id="http-definition",
                    project_id="project",
                    name="本地接口",
                    protocol="HTTP",
                    path="/before",
                    parameters={},
                    updated_by="owner",
                )
            )
            db.add(
                ApiTestEnvironment(
                    id="http-env",
                    project_id="project",
                    name="本地请求环境",
                    address="http://127.0.0.1:1",
                    updated_by="owner",
                )
            )
            db.flush()
            db.add(
                NativeCaseConfig(
                    case_id="case-0",
                    state="DONE",
                    api_definition_id="http-definition",
                    environment_id="http-env",
                    parameters={"request": {"headers": {"X-Frozen": "before"}}},
                    updated_by="owner",
                )
            )
            db.commit()
        # 分类配置和资源池从旧普通读快照切换到真实项目锁后的当前读。
        from services.plan_execution_config import (
            ConfigSave,
            ExecutionConfig,
            PoolSave,
            save,
            save_pool,
        )

        with Sessions() as db:
            pool = save_pool(
                db,
                db.get(TestPlan, "plan"),
                PoolSave(name="原池", environmentIds=["offline"]),
            )
            pool_id = pool.id
            save(
                db,
                db.get(TestPlan, "plan"),
                "root:api",
                ConfigSave(
                    config=ExecutionConfig(extended=False, testResourcePoolId=pool_id),
                    expectedRevision=0,
                ),
            )
            db.commit()
        ready, proceed = threading.Event(), threading.Event()

        def freeze_stale_config():
            with Sessions() as db:
                from services.plan_execution_config import ConfigurationTree

                plan = db.get(TestPlan, "plan")
                tree = ConfigurationTree(db, plan, dict(executionMode="serial"), [])
                assert tree.effective("root:api")["retryTimes"] == 1
                ready.set()
                assert proceed.wait(15)
                run = start(
                    db,
                    plan,
                    db.get(User, "owner"),
                    NativeWorkspaceRun(
                        category="api",
                        selectIds=["legacy:relation-0:case-0"],
                        requestId=str(uuid.uuid4()),
                    ),
                )
                item = db.query(PlanRunItem).filter_by(run_id=run.id).one()
                assert item.environment_id == "new-env"
                assert item.suite_snapshot["resourcePool"] == ["new-env"]
                assert item.suite_snapshot["executionConfig"]["retryTimes"] == 3
                assert item.suite_snapshot["nativeCases"][0]["retryTimes"] == 3
                db.rollback()
                return True

        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(freeze_stale_config)
            assert ready.wait(15)
            with Sessions() as holder:
                plan = holder.get(TestPlan, "plan")
                lock_project(holder, "project")
                save_pool(
                    holder,
                    plan,
                    PoolSave(
                        name="当前池", environmentIds=["new-env"], expectedRevision=1
                    ),
                    pool_id,
                )
                save(
                    holder,
                    plan,
                    "root:api",
                    ConfigSave(
                        config=ExecutionConfig(
                            extended=False,
                            testResourcePoolId=pool_id,
                            retryOnFailure=True,
                            retryTimes=3,
                            retryInterval=100,
                        ),
                        expectedRevision=1,
                    ),
                )
                holder.flush()
                proceed.set()
                for _ in range(100):
                    waits = root_sql(
                        "SELECT COUNT(*) FROM performance_schema.data_lock_waits w JOIN performance_schema.data_locks l ON w.REQUESTING_ENGINE_LOCK_ID=l.ENGINE_LOCK_ID WHERE l.OBJECT_SCHEMA='"
                        + name
                        + "'"
                    )
                    if int(waits or 0):
                        break
                    time.sleep(0.05)
                else:
                    raise AssertionError("未观察到配置冻结的真实项目锁等待")
                assert not future.done()
                holder.commit()
            assert future.result(timeout=15)
        log.info(
            "配置冻结通过：真实MySQL项目锁等待后读取最新资源池成员、重试次数及间隔；无实际派发"
        )

        def competing_save():
            with Sessions() as db:
                try:
                    save(
                        db,
                        db.get(TestPlan, "plan"),
                        "root:api",
                        ConfigSave(
                            config=ExecutionConfig(
                                extended=False, testResourcePoolId=pool_id, retryTimes=4
                            ),
                            expectedRevision=2,
                        ),
                    )
                    db.commit()
                    return 200
                except HTTPException as error:
                    db.rollback()
                    return error.status_code

        with ThreadPoolExecutor(max_workers=2) as executor:
            results = sorted(executor.map(lambda unused: competing_save(), range(2)))
        assert results == [200, 409], results
        log.info(
            "并发配置保存通过：相同旧版本两次提交分别返回200和409，未覆盖已提交配置"
        )
        print(
            "真实MySQL验收通过：原范围锁验证、最新资源池与步骤重试冻结、并发配置版本冲突；未派发执行。"
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
    main()
