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
        from sqlalchemy import create_engine, text
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
        with engine.connect() as check:
            rates = check.execute(
                text("SELECT ROUND(1.0 / 3, 2) * 100, ROUND(1.0 / 8, 2) * 100")
            ).one()
            assert tuple(rates) == (33, 13)
            log.info("MySQL官方比例舍入核验通过：1/3=%s%%，1/8=%s%%", *rates)
        Base.metadata.create_all(engine)
        Sessions = sessionmaker(bind=engine)
        from fastapi import HTTPException
        from models.case_governance import (
            CaseVersion,
            CaseReview,
            CaseReviewItem,
            CaseReviewDecision,
            CaseReviewEvent,
        )
        from models.review_workspace import ReviewWorkspace
        from schemas.case_governance import ReviewCreate, ReviewVote, ReviewHeader
        from schemas.review_workspace import ReviewAssociate
        from services.case_governance import create_review, vote_review
        from services.review_workspace import (
            archive_review,
            workspace,
            list_reviews,
            update_header,
            associate_cases,
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
            db.add(
                TestCase(
                    id="race-add-case",
                    project_id="race-project",
                    name="不能追加的用例",
                    case_code="RACE-ADD",
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
            empty = create_review(
                db,
                owner,
                "race-project",
                ReviewCreate(
                    name="追加成功验证", reviewerIds=[owner.id], mode="single"
                ),
            )
            first = associate_cases(
                db,
                owner,
                "race-project",
                empty.id,
                ReviewAssociate(caseIds=["race-case"], reviewerIds=[owner.id]),
            )
            kept_id = first["items"][0]["id"]
            vote_review(
                db,
                owner,
                "race-project",
                empty.id,
                kept_id,
                ReviewVote(decision="approved", comment="追加前有效结论"),
            )
            appended = associate_cases(
                db,
                owner,
                "race-project",
                empty.id,
                ReviewAssociate(caseIds=["race-add-case"], reviewerIds=[owner.id]),
            )
            kept = next(item for item in appended["items"] if item["id"] == kept_id)
            assert len(appended["items"]) == 2 and kept["status"] == "approved"
            assert kept["decisions"][0]["comment"] == "追加前有效结论"
            assert appended["status"] == "pending"
            db.commit()
        # 相同独立临时库核验生产 MySQL 的 JSON 人员筛选与真实分页。
        from services.review_case_workspace import listing
        from services.case_governance import review_data
        from models import Module

        with Sessions() as db:
            owner = db.get(User, "race-owner")
            parent = Module(
                id="page-parent", project_id="race-project", name="分页父模块"
            )
            child = Module(
                id="page-child",
                project_id="race-project",
                name="分页子模块",
                parent_id=parent.id,
            )
            db.add_all([parent, child])
            db.flush()
            case_ids = []
            for position in range(23):
                row = TestCase(
                    id=f"page-case-{position}",
                    project_id="race-project",
                    name=f"分页用例{position:02d}",
                    case_code=f"PAGE-{position:03d}",
                    type="functional",
                    priority="P3",
                    steps=[],
                    created_by=owner.id,
                    tags=["中文分页标签"] if position == 1 else [],
                    module_id=(
                        parent.id
                        if position == 0
                        else child.id if position == 1 else None
                    ),
                )
                db.add(row)
                case_ids.append(row.id)
            db.flush()
            paged = create_review(
                db,
                owner,
                "race-project",
                ReviewCreate(
                    name="数据库分页软件验收",
                    caseIds=case_ids,
                    reviewerIds=[owner.id],
                    mode="single",
                ),
            )
            db.commit()
            first = listing(
                db,
                owner,
                "race-project",
                paged.id,
                sort="caseCode",
                order="asc",
                only_mine=True,
            )
            second = listing(
                db,
                owner,
                "race-project",
                paged.id,
                page=2,
                sort="caseCode",
                order="asc",
                reviewer_id=owner.id,
            )
            assert (
                first["total"] == 23
                and len(first["items"]) == 20
                and len(second["items"]) == 3
            )
            assert not (
                {row["id"] for row in first["items"]}
                & {row["id"] for row in second["items"]}
            )
            assert (
                listing(db, owner, "race-project", paged.id, folder=parent.id)["total"]
                == 2
            )
            assert (
                listing(
                    db,
                    owner,
                    "race-project",
                    paged.id,
                    folder=parent.id,
                    include_descendants=False,
                )["total"]
                == 1
            )
            assert (
                listing(db, owner, "race-project", paged.id, search="中文分页标签")[
                    "total"
                ]
                == 1
            )
            assert first["counts"] == {"all": 23, "unassigned": 21}
            compact = review_data(db, paged, include_items=False)
            assert (
                compact["items"] == []
                and compact["caseCount"] == 23
                and compact["unReviewCount"] == 23
            )
            log.info(
                "MySQL关联列表核验通过：20+3分页、JSON评审人、中文标签、父子模块及无快照详情"
            )
        # 人员调整按最新名单重算，历史票保留，取消后重新关联不复用旧票。
        from models import ProjectMember
        from schemas.review_workspace import (
            ReviewItemReviewers,
            ReviewItemSelection,
            ReviewItemReReview,
        )
        from services.review_item_management import (
            change_reviewers,
            disassociate,
            re_review,
        )

        with Sessions() as db:
            owner = db.get(User, "race-owner")
            reader = User(
                id="page-reader",
                username="数据库评审人",
                email="page-reader@example.test",
                password_hash="不使用",
            )
            db.add(reader)
            db.flush()
            db.add(ProjectMember(project_id="race-project", user_id=reader.id))
            db.flush()
            multi = create_review(
                db,
                owner,
                "race-project",
                ReviewCreate(
                    name="人员修改数据库验收",
                    caseIds=["page-case-0"],
                    reviewerIds=[owner.id],
                    mode="multiple",
                ),
            )
            managed = db.query(CaseReviewItem).filter_by(review_id=multi.id).one()
            managed_id = managed.id
            vote_review(
                db,
                owner,
                "race-project",
                multi.id,
                managed.id,
                ReviewVote(decision="approved"),
            )
            added = change_reviewers(
                db,
                owner,
                "race-project",
                multi.id,
                ReviewItemReviewers(
                    itemIds=[managed.id], reviewerIds=[reader.id], append=True
                ),
            )
            assert added["underReviewedCount"] == 1 and added["lifecycle"] == "underway"
            changed = change_reviewers(
                db,
                owner,
                "race-project",
                multi.id,
                ReviewItemReviewers(itemIds=[managed.id], reviewerIds=[reader.id]),
            )
            assert (
                changed["underReviewedCount"] == 0
                and changed["unReviewCount"] == 1
                and changed["lifecycle"] == "prepared"
            )
            assert (
                list_reviews(
                    db,
                    owner,
                    "race-project",
                    lifecycle="prepared",
                    search="人员修改数据库验收",
                )["total"]
                == 1
            )
            assert (
                db.query(CaseReviewDecision).filter_by(item_id=managed.id).count() == 1
            )
            restored = change_reviewers(
                db,
                owner,
                "race-project",
                multi.id,
                ReviewItemReviewers(itemIds=[managed.id], reviewerIds=[owner.id]),
            )
            assert restored["passCount"] == 1 and restored["lifecycle"] == "completed"
            removed = disassociate(
                db,
                owner,
                "race-project",
                multi.id,
                ReviewItemSelection(itemIds=[managed.id]),
            )
            assert (
                removed["caseCount"] == 0
                and removed["lifecycle"] == "prepared"
                and removed["status"] == "pending"
            )
            new = associate_cases(
                db,
                owner,
                "race-project",
                multi.id,
                ReviewAssociate(caseIds=["page-case-0"], reviewerIds=[owner.id]),
            )
            assert (
                new["items"][0]["id"] != managed_id
                and not new["items"][0]["decisions"]
                and new["lifecycle"] == "prepared"
            )
            assert db.query(CaseVersion).count() == 25
            fresh_id = new["items"][0]["id"]
            vote_review(
                db,
                owner,
                "race-project",
                multi.id,
                fresh_id,
                ReviewVote(decision="approved"),
            )
            reset = re_review(
                db,
                owner,
                "race-project",
                multi.id,
                ReviewItemReReview(itemIds=[fresh_id], comment="<p>数据库重新提审</p>"),
            )
            assert reset["id"] == multi.id and reset["reReviewedCount"] == 1
            assert reset["reviewedCount"] == 0 and reset["lifecycle"] == "underway"
            assert (
                listing(db, owner, "race-project", multi.id, state="re_review")["total"]
                == 1
            )
            assert (
                list_reviews(
                    db,
                    owner,
                    "race-project",
                    lifecycle="underway",
                    search="人员修改数据库验收",
                )["total"]
                == 1
            )
            assert db.query(CaseReviewDecision).filter_by(item_id=fresh_id).count() == 0
            assert any(
                e["abandoned"] for e in reset["history"] if e["itemId"] == fresh_id
            )
            vote_review(
                db,
                owner,
                "race-project",
                multi.id,
                fresh_id,
                ReviewVote(decision="approved"),
            )
            assert (
                review_data(db, multi, include_items=False)["lifecycle"] == "completed"
            )
            assert db.query(CaseVersion).count() == 25
            db.commit()
            log.info(
                "MySQL人员与取消关联核验通过：追加/替换、按当前人员计数、历史票保留、全未评审及空评审未开始、重新关联新票"
            )
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

        ready_associate = threading.Event()

        def associator():
            with Sessions() as db:
                owner = db.get(User, "race-owner")
                review = db.get(CaseReview, identifier)
                assert workspace(db, review).archived is False
                ready_associate.set()
                assert start_vote.wait(15)
                try:
                    associate_cases(
                        db,
                        owner,
                        "race-project",
                        identifier,
                        ReviewAssociate(
                            caseIds=["race-add-case"], reviewerIds=[owner.id]
                        ),
                    )
                except HTTPException as error:
                    log.exception(
                        "并发验收捕获追加关联拒绝：状态=%s，原因=%s",
                        error.status_code,
                        error.detail,
                    )
                    rejected = error.status_code == 409 and "归档" in error.detail
                    db.rollback()
                    return rejected
                raise AssertionError("归档后追加关联未被拒绝")

        ready_management = threading.Event()

        def manager():
            with Sessions() as db:
                owner = db.get(User, "race-owner")
                review = db.get(CaseReview, identifier)
                assert workspace(db, review).archived is False
                ready_management.set()
                assert start_vote.wait(15)
                try:
                    change_reviewers(
                        db,
                        owner,
                        "race-project",
                        identifier,
                        ReviewItemReviewers(
                            itemIds=[item_id], reviewerIds=["page-reader"]
                        ),
                    )
                except HTTPException as error:
                    log.exception(
                        "并发验收捕获人员修改拒绝：状态=%s，原因=%s",
                        error.status_code,
                        error.detail,
                    )
                    rejected = error.status_code == 409 and "归档" in error.detail
                    db.rollback()
                    return rejected
                raise AssertionError("归档后人员修改未被拒绝")

        def archiver():
            with Sessions() as db:
                owner = db.get(User, "race-owner")
                archive_review(db, owner, "race-project", identifier)
                ready_b.set()
                assert release.wait(15)
                db.commit()

        ready_rereview = threading.Event()

        def rereviewer():
            with Sessions() as db:
                owner = db.get(User, "race-owner")
                review = db.get(CaseReview, identifier)
                assert workspace(db, review).archived is False
                ready_rereview.set()
                assert start_vote.wait(15)
                try:
                    re_review(
                        db,
                        owner,
                        "race-project",
                        identifier,
                        ReviewItemReReview(itemIds=[item_id]),
                    )
                except HTTPException as error:
                    log.exception(
                        "并发验收捕获同单重新提审拒绝：状态=%s，原因=%s",
                        error.status_code,
                        error.detail,
                    )
                    rejected = error.status_code == 409 and "归档" in error.detail
                    db.rollback()
                    return rejected
                raise AssertionError("归档后同单重新提审未被拒绝")

        with ThreadPoolExecutor(max_workers=5) as workers:
            voting = workers.submit(voter)
            assert ready_a.wait(15)
            associating = workers.submit(associator)
            assert ready_associate.wait(15)
            managing = workers.submit(manager)
            assert ready_management.wait(15)
            rereviewing = workers.submit(rereviewer)
            assert ready_rereview.wait(15)
            archiving = workers.submit(archiver)
            assert ready_b.wait(15)
            start_vote.set()
            observed = False
            for _ in range(15):
                count = root_sql(
                    "SELECT COUNT(*) FROM performance_schema.data_lock_waits w JOIN performance_schema.data_locks l ON w.REQUESTING_ENGINE_LOCK_ID=l.ENGINE_LOCK_ID WHERE l.OBJECT_SCHEMA="
                    + quote(name)
                )
                if count and int(count) >= 4:
                    observed = True
                    break
                time.sleep(0.1)
            release.set()
            archiving.result(15)
            rejected, stale = voting.result(15)
            add_rejected = associating.result(15)
            management_rejected = managing.result(15)
            rereview_rejected = rereviewing.result(15)
        assert (
            observed
            and rejected
            and stale
            and add_rejected
            and management_rejected
            and rereview_rejected
        )
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
            assert (
                db.query(CaseReviewEvent)
                .filter_by(review_id=identifier, action="重新提审")
                .count()
                == 0
            )
            assert len(review.name) == 255
            assert workspace(db, review).start_time.microsecond == 654321
            assert db.query(CaseReviewItem).filter_by(review_id=identifier).count() == 1
            assert db.query(CaseVersion).count() == 25
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
                "官方比例舍入33与13": True,
                "旧快照仍显示未归档": stale,
                "改投拒绝": rejected,
                "归档后追加关联拒绝": add_rejected,
                "空评审追加与保留有效票": True,
                "原结论未改变": True,
                "中文标签搜索": True,
                "255字符名称与微秒周期": True,
                "基本信息编辑保留有效票": True,
                "关联列表20加3分页及模块筛选": True,
                "人员修改与重新关联状态核验": True,
                "同单重新提审与有效票作废": True,
                "归档后四个实际等待者写入拒绝": management_rejected
                and rereview_rejected,
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
