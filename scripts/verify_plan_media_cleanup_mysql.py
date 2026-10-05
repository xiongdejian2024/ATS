"""使用原Docker MySQL的独立临时库验证清理与提交并发，不写原业务库。

需要本机ats-mysql容器及Docker执行权限；临时库和临时授权在finally中回收。
只运行数据库事务，不启动Agent、调度器或台架执行。
"""


def main():
    import sys, subprocess, json, uuid, logging, threading, time
    from pathlib import Path
    from concurrent.futures import ThreadPoolExecutor

    ROOT = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(ROOT / "backend"))
    (ROOT / "logs").mkdir(exist_ok=True)
    logging.basicConfig(
        filename=ROOT / "logs/plan-media-race.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    log = logging.getLogger("执行图片并发验收")
    name = "ats_media_race_" + uuid.uuid4().hex[:16]
    created = granted = False
    engine = None
    release = threading.Event()

    def root_sql(sql):
        result = subprocess.run(
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
            timeout=10,
            check=True,
        )
        return result.stdout.strip()

    try:
        import pymysql
        from sqlalchemy import create_engine
        from sqlalchemy.engine import URL
        from sqlalchemy.orm import sessionmaker
        from database import Base
        import models
        from models import User, Project, TestPlan, TestCase
        from models.plan_case_media import PlanCaseMedia, PlanCaseMediaLink
        from models.plan_case_execution import PlanCaseExecution
        from models.task_queue import TaskQueue
        from services.plan_case_media import cleanup_owned

        config = json.loads(
            subprocess.check_output(["docker", "inspect", "ats-mysql"])
        )[0]
        values = dict(
            item.split("=", 1) for item in config["Config"]["Env"] if "=" in item
        )
        connection = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user=values["MYSQL_USER"],
            password=values["MYSQL_PASSWORD"],
            database=values["MYSQL_DATABASE"],
        )
        with connection.cursor() as cursor:
            cursor.execute("SELECT CURRENT_USER()")
            principal = cursor.fetchone()[0]
        connection.close()
        account, host = principal.rsplit("@", 1)
        quote = lambda value: "'" + pymysql.converters.escape_string(value) + "'"
        root_sql(f"CREATE DATABASE `{name}` CHARACTER SET utf8mb4")
        created = True
        root_sql(
            f"GRANT ALL PRIVILEGES ON `{name}`.* TO {quote(account)}@{quote(host)}"
        )
        granted = True
        engine = create_engine(
            URL.create(
                "mysql+pymysql",
                username=values["MYSQL_USER"],
                password=values["MYSQL_PASSWORD"],
                host="127.0.0.1",
                port=3306,
                database=name,
            ),
            isolation_level="REPEATABLE READ",
        )
        Base.metadata.create_all(engine)
        Sessions = sessionmaker(bind=engine)
        identifier = str(uuid.uuid4())
        with Sessions() as db:
            db.add(
                User(
                    id="race-owner",
                    username="软件验收",
                    email="race@example.test",
                    password_hash="不使用的密码",
                )
            )
            db.flush()
            db.add(Project(id="race-project", name="临时并发库", owner_id="race-owner"))
            db.flush()
            db.add(
                TestPlan(
                    id="race-plan",
                    project_id="race-project",
                    owner_id="race-owner",
                    name="临时计划",
                    plan_number="RACE",
                )
            )
            db.flush()
            db.add(
                TestCase(
                    id="race-case",
                    project_id="race-project",
                    name="临时用例",
                    case_code="RACE",
                    type="functional",
                    steps=[],
                    created_by="race-owner",
                )
            )
            db.flush()
            db.add(
                PlanCaseMedia(
                    id=identifier,
                    plan_id="race-plan",
                    uploaded_by="race-owner",
                    file_name="软件验收.png",
                    file_size=8,
                    mime_type="image/png",
                    content=b"software",
                )
            )
            db.commit()
        ready_a = threading.Event()
        ready_b = threading.Event()
        start_cleanup = threading.Event()

        def cleaner():
            with Sessions() as db:
                owner = db.get(User, "race-owner")
                plan = db.get(TestPlan, "race-plan")
                assert (
                    db.query(PlanCaseMediaLink).filter_by(media_id=identifier).first()
                    is None
                )
                ready_a.set()
                assert start_cleanup.wait(15)
                outcome = cleanup_owned(db, owner, plan, [identifier])
                stale = (
                    db.query(PlanCaseMediaLink).filter_by(media_id=identifier).first()
                    is None
                )
                db.commit()
                return outcome, stale

        def writer():
            with Sessions() as db:
                db.query(PlanCaseMedia).filter_by(id=identifier).with_for_update().one()
                execution = PlanCaseExecution(
                    plan_id="race-plan",
                    association_key="软件并发关联",
                    case_id="race-case",
                    request_id=str(uuid.uuid4()),
                    payload_hash="0" * 64,
                    executor_id="race-owner",
                    executor_name="软件验收",
                    result="passed",
                    description="已提交证据",
                    case_snapshot={},
                )
                db.add(execution)
                db.flush()
                db.add(
                    PlanCaseMediaLink(execution_id=execution.id, media_id=identifier)
                )
                db.flush()
                ready_b.set()
                assert release.wait(15)
                db.commit()

        with ThreadPoolExecutor(max_workers=2) as workers:
            cleaning = workers.submit(cleaner)
            assert ready_a.wait(15)
            writing = workers.submit(writer)
            assert ready_b.wait(15)
            start_cleanup.set()
            observed = False
            for _ in range(15):
                count = root_sql(
                    "SELECT COUNT(*) FROM performance_schema.data_lock_waits w JOIN performance_schema.data_locks l ON w.REQUESTING_ENGINE_LOCK_ID=l.ENGINE_LOCK_ID WHERE l.OBJECT_SCHEMA="
                    + quote(name)
                )
                if count and int(count) > 0:
                    observed = True
                    break
                time.sleep(0.1)
            release.set()
            writing.result(15)
            outcome, stale = cleaning.result(15)
        assert (
            observed
            and stale
            and outcome == dict(removed=[], retained=[identifier], missing=[])
        )
        with Sessions() as db:
            assert (
                db.query(PlanCaseMedia).count() == 1
                and db.query(PlanCaseMediaLink).count() == 1
                and db.query(PlanCaseExecution).count() == 1
                and db.query(TaskQueue).count() == 0
            )
        log.info(
            "MySQL重复读并发验收通过：真实锁等待=%s，旧快照不可见=%s，当前读保留历史图片；原业务库未写入",
            observed,
            stale,
        )
        print(
            {
                "真实MySQL锁等待": observed,
                "旧快照未看到引用": stale,
                "当前读保留历史图片": True,
                "节点任务": 0,
            }
        )
    except Exception:
        log.exception("MySQL执行图片并发验收失败")
        raise
    finally:
        release.set()
        if engine is not None:
            engine.dispose()
        if created:
            try:
                if granted:
                    root_sql(
                        f"REVOKE ALL PRIVILEGES ON `{name}`.* FROM {quote(account)}@{quote(host)}"
                    )
                root_sql(f"DROP DATABASE `{name}`")
                log.info("自建临时验收库与临时授权已清理：%s", name)
            except Exception:
                log.exception("清理自建临时验收库失败：%s", name)
                raise


if __name__ == "__main__":
    main()
