"""在独立临时MySQL库验证规划脑图当前读、并发保存和删除，不入队或执行台架。"""

import json
import logging
from pathlib import Path
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
logging.basicConfig(
    filename=ROOT / "logs/第57部分MySQL验收.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("规划脑图数据库验收")


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
    name = "ats_minder_edit_" + uuid.uuid4().hex[:16]
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
        from models import TestPlan, TestSuite, PlanCaseRelation
        from models.plan_workspace import PlanNode
        from services.plan_minder_edit import load, save, MinderSave
        from services.review_workspace import lock_project

        with Sessions() as db:
            db.add(
                User(
                    id="owner",
                    username="规划验收",
                    email="minder@example.test",
                    password_hash="不登录",
                )
            )
            db.flush()
            db.add(Project(id="project", name="独立规划项目", owner_id="owner"))
            db.flush()
            db.add(
                TestPlan(
                    id="plan",
                    project_id="project",
                    owner_id="owner",
                    name="规划验收",
                    plan_number="MINDER",
                )
            )
            db.flush()
            for i in range(2):
                db.add(
                    TestCase(
                        id=f"case-{i}",
                        project_id="project",
                        case_code=f"CODE-{i}",
                        name=f"主用例{i}",
                        type="functional",
                        is_automated=False,
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
            db.commit()
            initial = load(db, db.get(User, "owner"), "plan")
            db.commit()
        identifier = str(uuid.uuid4())
        body = MinderSave(
            expectedFingerprint=initial["fingerprint"],
            points=[
                dict(id=identifier, name="并发新增", category="functional", position=0)
            ],
        )

        def attempt():
            with Sessions() as db:
                try:
                    save(db, db.get(User, "owner"), "plan", body)
                    db.commit()
                    return 200
                except HTTPException as exc:
                    log.exception("预期的旧规划冲突，事务回滚")
                    db.rollback()
                    return exc.status_code

        with ThreadPoolExecutor(max_workers=2) as executor:
            results = sorted(executor.map(lambda unused: attempt(), range(2)))
        assert results == [200, 409], results
        log.info("相同旧指纹并发保存分别200/409，只有一个测试集落库")
        with Sessions() as stale:
            # 先建立旧普通读快照，再让另一事务持有项目锁并增关联。
            user = stale.get(User, "owner")
            old = load(stale, user, "plan")
            stale.commit()
            stale.get(TestPlan, "plan")
            with Sessions() as holder, ThreadPoolExecutor(max_workers=1) as executor:
                lock_project(holder, "project")
                entered = threading.Event()
                updated = MinderSave(
                    expectedFingerprint=old["fingerprint"],
                    points=[
                        dict(
                            id=identifier,
                            name="不应覆盖",
                            category="functional",
                            position=0,
                        )
                    ],
                )

                def waiter():
                    entered.set()
                    try:
                        save(stale, user, "plan", updated)
                        stale.commit()
                        return 200
                    except HTTPException as exc:
                        log.exception("预期的当前读关联冲突，事务回滚")
                        stale.rollback()
                        return exc.status_code

                future = executor.submit(waiter)
                assert entered.wait(3)
                for _ in range(60):
                    waits = root_sql(
                        "SELECT COUNT(*) FROM performance_schema.data_lock_waits"
                    )
                    if int(waits or 0):
                        break
                    time.sleep(0.05)
                else:
                    raise AssertionError("未观察到规划保存的真实项目锁等待")
                assert not future.done()
                holder.add(
                    TestCase(
                        id="case-new",
                        project_id="project",
                        case_code="NEW",
                        name="另一页用例",
                        type="functional",
                        is_automated=False,
                        steps=[],
                        created_by="owner",
                    )
                )
                holder.flush()
                holder.add(
                    PlanCaseRelation(
                        id="new-relation",
                        plan_id="plan",
                        case_id="case-new",
                        execution_order=2,
                    )
                )
                holder.commit()
                assert future.result(timeout=15) == 409
        with Sessions() as db:
            assert db.get(PlanNode, identifier).name == "并发新增"
            assert db.query(PlanCaseRelation).count() == 3
            assert db.query(TaskQueue).count() == 0
            current = load(db, db.get(User, "owner"), "plan")
            db.commit()
            save(
                db,
                db.get(User, "owner"),
                "plan",
                MinderSave(
                    expectedFingerprint=current["fingerprint"],
                    points=[
                        dict(
                            id=identifier,
                            name="默认集实体",
                            category="functional",
                            position=0,
                        )
                    ],
                    deleteDefaults=["functional"],
                ),
            )
            db.commit()
            assert db.query(PlanCaseRelation).count() == 0
            assert db.query(TestCase).count() == 3
        log.info(
            "真实项目锁等待后读取最新关联并拒绝旧指纹；删除默认集仅取消关联，主用例保留，无任何队列任务"
        )
        print(
            "真实MySQL规划验收通过：相同指纹并发200/409；旧快照等待项目锁后拒绝覆盖新增关联；默认集取消关联，主用例保留，无派发。"
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
