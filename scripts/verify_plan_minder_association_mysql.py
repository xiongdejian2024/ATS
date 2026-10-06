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
    filename=ROOT / "logs/第62部分MySQL验收.log",
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
            for i in range(2):
                db.add(
                    TestCase(
                        id=f"case-{i}",
                        project_id="project",
                        case_code=f"DRAFT-{i}",
                        name=f"主用例{i}",
                        type="functional",
                        is_automated=False,
                        steps=[],
                        created_by="owner",
                    )
                )
            db.commit()
            user = db.get(User, "owner")
            initial = load(db, user, "plan")
            db.commit()
            identifier = str(uuid.uuid4())
            draft = MinderSave(
                expectedFingerprint=initial["fingerprint"],
                points=[
                    dict(
                        id=identifier,
                        name="临时关联集",
                        category="functional",
                        parentId=None,
                        position=0,
                    )
                ],
            )
            chosen = CandidateSelection(caseIds=["case-0"])
            for _ in range(2):
                result = preview_candidates(
                    db,
                    user,
                    "plan",
                    MinderCandidatePreview(draft=draft, selection=chosen),
                )
                db.commit()
                assert (
                    result["count"] == 1
                    and db.query(PlanNode).count()
                    == db.query(PlanCaseRelation).count()
                    == 0
                )
                assert load(db, user, "plan")["fingerprint"] == initial["fingerprint"]
                db.commit()
            draft.associations = [
                Association(caseIds=["case-0"], collectionId=identifier),
                Association(caseIds=["missing"]),
            ]
            try:
                save(db, user, "plan", draft)
            except HTTPException as exc:
                db.rollback()
                log.exception("预期关联晚期校验拒绝，验证整图回滚")
                assert exc.status_code == 404
            else:
                raise AssertionError("缺失用例未被拒绝")
            assert db.query(PlanNode).count() == db.query(PlanCaseRelation).count() == 0
            draft.associations = draft.associations[:1]
            saved = save(db, user, "plan", draft)
            db.commit()
            assert (
                db.get(PlanNode, identifier)
                and db.query(PlanCaseRelation).one().collection_id == identifier
            )
            assert db.query(TestCase).count() == 2 and db.query(TaskQueue).count() == 0
            try:
                save(db, user, "plan", draft)
            except HTTPException as exc:
                db.rollback()
                log.exception("预期旧指纹被拒绝")
                assert exc.status_code == 409
            else:
                raise AssertionError("旧关联草稿未被拒绝")
            log.info(
                "MySQL两次预览均完整回滚；关联晚期404撤销临时集与先前关联；真实保存及旧指纹409通过；两主用例保留，任务0"
            )
            print(
                "MySQL关联草稿验收通过：预览不留记录、晚期整图回滚、同次新增关联、旧指纹409、无任务。"
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
