"""在调用方的独立临时库中验证范围全选当前读和归档等待，不接台架。"""

import threading
import time
from concurrent.futures import ThreadPoolExecutor
from fastapi import HTTPException
from models import User
from models.case_governance import CaseReviewItem, CaseReviewDecision, CaseVersion
from models.task_queue import TaskQueue
from schemas.case_governance import ReviewCreate, ReviewVote
from schemas.review_workspace import ReviewItemVote, ReviewItemSelection
from services.case_governance import create_review, vote_review, vote_reviews
from services.review_item_selection import preview, vote, apply
from services.review_item_management import disassociate
from services.review_workspace import lock_project, archive_review


def verify_selection(Sessions, root_sql, name, log):
    with Sessions() as db:
        owner = db.get(User, "race-owner")
        review = create_review(
            db,
            owner,
            "race-project",
            ReviewCreate(
                name="范围全选数据库验收",
                caseIds=[f"page-case-{i}" for i in range(23)],
                reviewerIds=["race-owner", "page-reader"],
                mode="multiple",
            ),
        )
        identifier = review.id
        items = {
            i.case_id: i.id
            for i in db.query(CaseReviewItem).filter_by(review_id=identifier).all()
        }
        first, excluded = items["page-case-0"], items["page-case-2"]
        db.commit()
        before = db.query(CaseVersion).count()
    scope = ReviewItemVote(
        selectAll=True,
        excludeIds=[excluded],
        condition={"state": "un_review"},
        decision="rejected",
        comment="范围当前读软件理由",
    )
    ready, proceed = threading.Event(), threading.Event()

    def await_lock():
        for _ in range(100):
            count = root_sql(
                "SELECT COUNT(*) FROM performance_schema.data_lock_waits w JOIN performance_schema.data_locks l ON w.REQUESTING_ENGINE_LOCK_ID=l.ENGINE_LOCK_ID WHERE l.OBJECT_SCHEMA='"
                + name
                + "'"
            )
            if int(count or 0):
                return True
            time.sleep(0.05)
        return False

    def scoped_voter():
        with Sessions() as db:
            owner = db.get(User, "race-owner")
            assert preview(db, owner, "race-project", identifier, scope)["count"] == 22
            ready.set()
            assert proceed.wait(15)
            result = vote(db, owner, "race-project", identifier, scope)
            db.commit()
            return result["unPassCount"]

    try:
        with ThreadPoolExecutor(max_workers=1) as pool:
            pending = pool.submit(scoped_voter)
            assert ready.wait(15)
            try:
                with Sessions() as holder:
                    owner = holder.get(User, "race-owner")
                    lock_project(holder, "race-project")
                    vote_review(
                        holder,
                        owner,
                        "race-project",
                        identifier,
                        first,
                        ReviewVote(decision="approved"),
                    )
                    proceed.set()
                    waited = await_lock()
                    assert waited and not pending.done()
                    holder.commit()
                assert pending.result(timeout=15) == 21
            finally:
                proceed.set()
        with Sessions() as db:
            votes = {
                d.item_id: d.decision
                for d in db.query(CaseReviewDecision)
                .join(CaseReviewItem)
                .filter(CaseReviewItem.review_id == identifier)
                .all()
            }
            assert (
                votes[first] == "approved"
                and excluded not in votes
                and len(votes) == 22
            )
            assert db.query(CaseVersion).count() == before
            owner = db.get(User, "race-owner")
            # 排除项跨所有页保持；用例主记录及版本不被取消关联改写。
            selection = ReviewItemSelection(
                selectAll=True,
                excludeIds=[first, excluded],
                condition={"state": "rejected"},
            )
            result = apply(
                db,
                owner,
                "race-project",
                identifier,
                selection,
                lambda chosen: disassociate(
                    db, owner, "race-project", identifier, chosen
                ),
            )
            assert result["caseCount"] == 2 and db.query(CaseVersion).count() == before
            db.commit()
            remaining = [
                i.id
                for i in db.query(CaseReviewItem).filter_by(review_id=identifier).all()
            ]
            for person in [owner, db.get(User, "page-reader")]:
                vote_reviews(
                    db,
                    person,
                    "race-project",
                    identifier,
                    remaining,
                    ReviewVote(decision="approved"),
                )
            db.commit()
        log.info(
            "MySQL范围全选当前读验证通过：预读22条，实际等待项目锁后跳过新评审中条目，仅写21条，排除项无票，取消关联后版本不变"
        )

        ready.clear()
        proceed.clear()

        def archived_selector():
            with Sessions() as db:
                owner = db.get(User, "race-owner")
                assert preview(
                    db,
                    owner,
                    "race-project",
                    identifier,
                    ReviewItemSelection(selectAll=True),
                )["canVote"]
                ready.set()
                assert proceed.wait(15)
                try:
                    vote(
                        db,
                        owner,
                        "race-project",
                        identifier,
                        ReviewItemVote(
                            selectAll=True,
                            decision="rejected",
                            comment="归档后不得改写",
                        ),
                    )
                except HTTPException as error:
                    log.exception(
                        "MySQL范围全选归档等待者被拒绝：HTTP=%s 原因=%s",
                        error.status_code,
                        error.detail,
                    )
                    db.rollback()
                    return error.status_code == 409 and "归档" in error.detail
                raise AssertionError("归档后范围全选写入未被拒绝")

        with ThreadPoolExecutor(max_workers=1) as pool:
            pending = pool.submit(archived_selector)
            assert ready.wait(15)
            try:
                with Sessions() as holder:
                    archive_review(
                        holder,
                        holder.get(User, "race-owner"),
                        "race-project",
                        identifier,
                    )
                    proceed.set()
                    archived_waited = await_lock()
                    assert archived_waited and not pending.done()
                    holder.commit()
                assert pending.result(timeout=15)
            finally:
                proceed.set()
        with Sessions() as db:
            assert all(
                d.decision == "approved"
                for d in db.query(CaseReviewDecision)
                .join(CaseReviewItem)
                .filter(CaseReviewItem.review_id == identifier)
                .all()
            )
            assert (
                db.query(CaseVersion).count() == before
                and db.query(TaskQueue).count() == 0
            )
        log.info(
            "MySQL范围全选归档等待核验通过：实际等待后409，已有通过票、版本和任务数量保持"
        )
        return {
            "范围全选当前读真实等待": waited,
            "范围全选排除与取消关联": True,
            "范围全选归档等待拒绝": archived_waited,
        }
    finally:
        proceed.set()
