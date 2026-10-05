"""在独立临时MySQL库验证关联全范围锁内当前读和并发提交，不执行台架。"""

import json
import logging
from pathlib import Path
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
logging.basicConfig(
    filename=ROOT / "logs/第47部分MySQL验收.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("计划关联范围数据库验收")


def main():
    import pymysql
    from sqlalchemy import create_engine
    from sqlalchemy.engine import URL
    from sqlalchemy.orm import sessionmaker
    from database import Base
    import models
    from models import User, Project, TestCase
    from models.case_governance import CaseSavedView, CaseVersion
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
    name = "ats_candidate_scope_" + uuid.uuid4().hex[:16]
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
        import threading
        import time
        from datetime import datetime
        from fastapi import HTTPException
        from models import TestPlan, PlanCaseRelation, TestExecution, Module
        from models.plan_workspace import PlanWorkspace, PlanNode
        from models.native_case import ApiDefinition, ApiTestEnvironment, NativeCaseConfig
        from schemas.plan_candidate_selection import Association
        from services.plan_candidate_selection import preview
        from services.plan_case_workspace import associate
        from services.native_case import fingerprint
        from services.review_workspace import lock_project
        from api.v1.case_governance import transact
        steps = [dict(action=f"步骤{i}", expected="已保存") for i in range(3)]
        with Sessions() as db:
            owner = User(id="owner", username="范围验收", email="scope@example.test", password_hash="不登录")
            db.add(owner); db.flush()
            db.add(Project(id="project", name="独立范围验收", owner_id=owner.id)); db.flush()
            db.add_all([TestPlan(id=pid, project_id="project", owner_id="owner", name=pid, plan_number=pid) for pid in ["plan", "source"]]); db.flush()
            db.add(PlanWorkspace(plan_id="plan", uses_tree=False))
            db.add(Module(id="parent", project_id="project", name="父模块")); db.flush()
            db.add(Module(id="child", project_id="project", name="子模块", parent_id="parent")); db.flush()
            db.add(ApiTestEnvironment(id="env", project_id="project", name="真实环境", address="不发送网络请求", updated_by="owner")); db.flush()
            for i in range(23):
                db.add(TestCase(id=f"manual-{i}", project_id="project", name=f"手工范围{i}", case_code=f"MANUAL-{i}", type="functional", priority="P1", steps=[], module_id="child", is_automated=False, created_by="owner"))
            for i in range(3):
                db.add(ApiDefinition(id=f"def-{i}", project_id="project", name=f"接口{i}", protocol="HTTP", path=f"/接口/{i}", parameters={}, updated_by="owner")); db.flush()
                db.add_all([TestCase(id=f"api-{i}", project_id="project", name=f"接口范围{i}", case_code=f"API-{i}", type="api", priority="P1", steps=[], is_automated=True, created_by="owner"),
                            TestCase(id=f"scene-{i}", project_id="project", name=f"场景范围{i}", case_code=f"SCENE-{i}", type="scenario", priority="P1", steps=steps, is_automated=True, created_by="owner")]); db.flush()
                db.add(NativeCaseConfig(case_id=f"api-{i}", state="PROCESSING", api_definition_id=f"def-{i}", environment_id="env", parameters={}, definition_fingerprint=fingerprint({}), updated_by="owner"))
                db.add(NativeCaseConfig(case_id=f"scene-{i}", state="UNDERWAY", environment_id="env", parameters={}, updated_by="owner"))
                db.add(TestExecution(id=f"report-{i}", case_id=f"api-{i}", executor_id="owner", result="passed", executed_at=datetime(2026, 10, 6)))
                db.add(PlanCaseRelation(plan_id="source", case_id=f"api-{i}"))
            db.commit()
        c = lambda field, operator, value: dict(field=field, operator=operator, value=value)
        api_scope = lambda *conditions: dict(category="api", selectAll=True, excludeIds=["api-2"], condition=dict(filters=dict(conditions=list(conditions))))
        manual_scope = dict(selectAll=True, excludeIds=["manual-22"], condition=dict(search="手工范围", priority="P1", folder="parent"))
        trials = [
            ("基本优先级", manual_scope, 22, 21),
            ("模块层级", manual_scope, 22, 0),
            ("原生状态", api_scope(c("nativeState", "equals", "PROCESSING")), 2, 1),
            ("原生环境", api_scope(c("environmentName", "equals", "env")), 2, 1),
            ("定义参数变更", api_scope(c("apiChange", "equals", False)), 2, 1),
            ("最近真实执行结果", api_scope(c("lastReportStatus", "equals", "SUCCESS")), 2, 1),
            ("所属计划关系", api_scope(c("planIds", "equals", "source")), 2, 1),
            ("场景步骤数", dict(category="scenario", selectAll=True, excludeIds=["scene-2"], condition=dict(filters=dict(conditions=[c("stepTotal", "equals", 3)]))), 2, 1),
            ("归档状态", manual_scope, 22, 0),
            ("树范围切换", manual_scope, 22, 22),
        ]
        for label, payload, before, after in trials:
            ready, proceed = threading.Event(), threading.Event()
            body = Association(**payload)
            def waiting_writer():
                with Sessions() as db:
                    owner, plan = db.get(User, "owner"), db.get(TestPlan, "plan")
                    assert preview(db, plan, owner, body)["count"] == before
                    ready.set(); assert proceed.wait(15)
                    try:
                        result = associate(db, plan, owner, body)["added"]
                    except HTTPException as exc:
                        log.exception("预期范围为空或计划已归档，整批拒绝：%s", label)
                        assert exc.status_code == 409
                        result = 0
                    finally:
                        db.rollback()
                    return result
            with ThreadPoolExecutor(max_workers=1) as pool:
                pending = pool.submit(waiting_writer)
                if not ready.wait(15):
                    pending.result(timeout=1)
                    raise RuntimeError("范围预览未就绪")
                try:
                    with Sessions() as holder:
                        lock_project(holder, "project")
                        if label == "基本优先级": holder.get(TestCase, "manual-0").priority = "P0"
                        elif label == "模块层级": holder.get(Module, "child").parent_id = None
                        elif label == "原生状态": holder.get(NativeCaseConfig, "api-0").state = "DONE"
                        elif label == "原生环境": holder.get(NativeCaseConfig, "api-0").environment_id = None
                        elif label == "定义参数变更": holder.get(ApiDefinition, "def-0").parameters = {"新增": False}
                        elif label == "最近真实执行结果": holder.get(TestExecution, "report-0").result = "failed"
                        elif label == "所属计划关系": holder.query(PlanCaseRelation).filter_by(plan_id="source", case_id="api-0").delete()
                        elif label == "场景步骤数": holder.get(TestCase, "scene-0").steps = steps + [dict(action="第4步", expected="新结果")]
                        elif label == "归档状态": holder.get(PlanWorkspace, "plan").archived = True
                        else: holder.get(PlanWorkspace, "plan").uses_tree = True
                        holder.flush(); proceed.set()
                        waited = False
                        for _ in range(100):
                            waits = root_sql("SELECT COUNT(*) FROM performance_schema.data_lock_waits w JOIN performance_schema.data_locks l ON w.REQUESTING_ENGINE_LOCK_ID=l.ENGINE_LOCK_ID WHERE l.OBJECT_SCHEMA='" + name + "'")
                            if int(waits or 0): waited = True; break
                            time.sleep(.05)
                        assert waited and not pending.done(), label
                        holder.commit()
                    assert pending.result(timeout=15) == after, label
                    log.info("%s通过：旧预览%s、真实等待项目锁、锁内当前读%s、写入回滚，跨页排除保持", label, before, after)
                finally: proceed.set()
            with Sessions() as restore:
                restore.get(TestCase, "manual-0").priority = "P1"
                restore.get(Module, "child").parent_id = "parent"
                cfg = restore.get(NativeCaseConfig, "api-0"); cfg.state = "PROCESSING"; cfg.environment_id = "env"
                restore.get(ApiDefinition, "def-0").parameters = {}
                restore.get(TestExecution, "report-0").result = "passed"
                restore.get(TestCase, "scene-0").steps = steps
                ws = restore.get(PlanWorkspace, "plan"); ws.archived = False; ws.uses_tree = False
                if not restore.query(PlanCaseRelation).filter_by(plan_id="source", case_id="api-0").first():
                    restore.add(PlanCaseRelation(plan_id="source", case_id="api-0"))
                restore.commit()
                assert restore.query(PlanCaseRelation).filter_by(plan_id="plan").count() == 0
                assert restore.query(PlanNode).count() == 0 and restore.query(TaskQueue).count() == 0
        def concurrent_association(index):
            with Sessions() as db:
                try:
                    transact(db, lambda: associate(db, db.get(TestPlan, "plan"), db.get(User, "owner"), Association(**manual_scope)))
                    return 200
                except HTTPException as exc:
                    return exc.status_code
        with ThreadPoolExecutor(max_workers=2) as pool:
            assert sorted(pool.map(concurrent_association, [0, 1])) == [200, 409]
        with Sessions() as db:
            assert {r.case_id for r in db.query(PlanCaseRelation).filter_by(plan_id="plan")} == {f"manual-{i}" for i in range(22)}
            assert db.query(CaseVersion).count() == 0 and db.query(TaskQueue).count() == 0
        log.info("并发重复范围关联单胜：200/409，实际22条且无重复；版本与节点任务均0")
        print("真实MySQL十种锁内当前读和并发关联验收通过；未运行台架")
    except Exception:
        log.exception("真实MySQL关联范围验收失败")
        raise
    finally:
        if engine is not None:engine.dispose()
        if granted:root_sql(f"REVOKE ALL PRIVILEGES ON `{name}`.* FROM {quote(account)}@{quote(host)}")
        if created:root_sql(f"DROP DATABASE `{name}`")
        log.info("独立临时库与临时授权已回收：%s",name)

if __name__=="__main__":main()
