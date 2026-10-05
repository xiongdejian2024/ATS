"""使用原Docker MySQL的独立临时库验证归档与投票并发，不写原业务库。

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
        filename=ROOT / "logs/review-archive-race.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    log = logging.getLogger("评审归档并发验收")
    name = "ats_review_race_" + uuid.uuid4().hex[:16]
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
        from models import User, Project, TestCase
        from models.task_queue import TaskQueue

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
        from fastapi import HTTPException
        from models.case_governance import (
            CaseReview,
            CaseReviewItem,
            CaseReviewDecision,
            CaseReviewEvent,
        )
        from models.review_workspace import ReviewWorkspace
        from schemas.case_governance import ReviewCreate, ReviewVote, ReviewHeader
        from services.case_governance import create_review, vote_review
        from services.review_workspace import (
            archive_review,
            workspace,
            list_reviews,
            update_header,
        )

        with Sessions() as db:
            owner = User(
                id="race-owner",
                username="软件验收",
                email="race@example.test",
                password_hash="不使用",
            )
            db.add(owner)
            db.flush()
            db.add(Project(id="race-project", name="评审临时并发库", owner_id=owner.id))
            db.flush()
            db.add(
                TestCase(
                    id="race-case",
                    project_id="race-project",
                    name="软件用例",
                    case_code="RACE",
                    type="functional",
                    steps=[],
                    created_by=owner.id,
                )
            )
            db.flush()
            review = create_review(
                db,
                owner,
                "race-project",
                ReviewCreate(
                    name="评" * 255,
                    startTime="2026-10-05T01:30:01.123456Z",
                    endTime="2026-10-05T10:00:00+08:00",
                    caseIds=["race-case"],
                    reviewerIds=[owner.id],
                    mode="single",
                    tags=["中文标签"],
                ),
            )
            item = db.query(CaseReviewItem).filter_by(review_id=review.id).one()
            identifier, item_id = review.id, item.id
            vote_review(
                db,
                owner,
                "race-project",
                identifier,
                item_id,
                ReviewVote(decision="approved", comment="完成软件评审"),
            )
            db.commit()
            db.expire_all()
            stored = workspace(db, review)
            assert stored.start_time.microsecond == 123456
            edited = update_header(
                db,
                owner,
                "race-project",
                identifier,
                ReviewHeader(
                    name="审" * 255,
                    reviewerIds=[owner.id],
                    mode="single",
                    tags=["中文标签"],
                    startTime="2026-10-05T09:45:01.654321+08:00",
                    endTime="2026-10-05T10:15:00+08:00",
                ),
            )
            assert edited["startTime"] == "2026-10-05T09:45:01.654321+08:00"
            assert edited["items"][0]["id"] == item_id
            assert edited["items"][0]["decisions"][0]["decision"] == "approved"
            db.commit()
        ready_a, ready_b, start_vote = (
            threading.Event(),
            threading.Event(),
            threading.Event(),
        )

        def voter():
            with Sessions() as db:
                owner = db.get(User, "race-owner")
                review = db.get(CaseReview, identifier)
                assert workspace(db, review).archived is False
                ready_a.set()
                assert start_vote.wait(15)
                try:
                    vote_review(
                        db,
                        owner,
                        "race-project",
                        identifier,
                        item_id,
                        ReviewVote(decision="rejected", comment="不能覆盖归档"),
                    )
                except HTTPException as error:
                    log.exception(
                        "并发验收捕获评审写入拒绝：状态=%s，原因=%s",
                        error.status_code,
                        error.detail,
                    )
                    rejected = error.status_code == 409 and "归档" in error.detail
                    # 再次普通查询仍可能读取旧快照，当前读检查已经拒绝修改。
                    stale = (
                        db.query(ReviewWorkspace.archived)
                        .filter_by(review_id=identifier)
                        .scalar()
                        is False
                    )
                    db.rollback()
                    return rejected, stale
                raise AssertionError("归档后改投未被拒绝")

        def archiver():
            with Sessions() as db:
                owner = db.get(User, "race-owner")
                archive_review(db, owner, "race-project", identifier)
                ready_b.set()
                assert release.wait(15)
                db.commit()

        with ThreadPoolExecutor(max_workers=2) as workers:
            voting = workers.submit(voter)
            assert ready_a.wait(15)
            archiving = workers.submit(archiver)
            assert ready_b.wait(15)
            start_vote.set()
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
            archiving.result(15)
            rejected, stale = voting.result(15)
        assert observed and rejected and stale
        with Sessions() as db:
            review = db.get(CaseReview, identifier)
            assert workspace(db, review).archived is True
            assert (
                db.query(CaseReviewDecision).filter_by(item_id=item_id).one().decision
                == "approved"
            )
            assert (
                db.query(CaseReviewEvent)
                .filter_by(review_id=identifier, action="评审结论")
                .count()
                == 1
            )
            assert len(review.name) == 255
            assert workspace(db, review).start_time.microsecond == 654321
            assert db.query(TaskQueue).count() == 0
            owner = db.get(User, "race-owner")
            summary = list_reviews(
                db, owner, "race-project", lifecycle="archived", search="中文标签"
            )
            assert summary["total"] == 1 and summary["items"][0]["passRate"] == 100
            assert (
                summary["items"][0]["startTime"] == "2026-10-05T09:45:01.654321+08:00"
            )
        log.info(
            "MySQL评审并发验收通过：真实锁等待=%s，旧快照=%s，归档后改投已拒绝，历史结论保持通过；原业务库未写入",
            observed,
            stale,
        )
        print(
            {
                "真实MySQL锁等待": observed,
                "旧快照仍显示未归档": stale,
                "改投拒绝": rejected,
                "原结论未改变": True,
                "中文标签搜索": True,
                "255字符名称与微秒周期": True,
                "基本信息编辑保留有效票": True,
                "节点任务": 0,
            }
        )
    except Exception:
        log.exception("MySQL评审归档并发验收失败")
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
