"""在独立临时MySQL库验证主用例范围等待锁后的当前读，不执行台架。"""

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
    filename=ROOT / "logs/第43部分MySQL验收.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("主用例范围数据库验收")


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
    name = "ats_case_scope_" + uuid.uuid4().hex[:16]
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
        from models.case_features import CaseFollow, CaseIssue, CaseIssueLink
        from models.test_case import CaseAttachment
        from schemas.case_selection import CaseSelection
        from schemas.case_governance import CaseBatchUpdate, ReviewCreate, ReviewVote
        from services.case_selection import preview
        from services.case_governance import batch_update, create_review, vote_review
        from services.review_workspace import lock_project
        with Sessions() as db:
            owner=User(id="scope-owner",username="范围验收",email="scope@example.test",password_hash="不登录")
            db.add(owner);db.flush()
            db.add(Project(id="scope-project",name="范围独立临时库",owner_id=owner.id));db.flush()
            db.add_all([TestCase(id=f"scope-{i}",project_id="scope-project",name=f"范围{i}",case_code=f"SCOPE-{i}",type="functional",priority="P1",steps=[],created_by=owner.id) for i in range(23)])
            db.flush()
            db.add_all([CaseFollow(case_id=f"scope-{i}",user_id=owner.id) for i in range(23)])
            db.add_all([CaseAttachment(case_id=f"scope-{i}",file_name="当前附件.txt",file_path="不读取文件",uploaded_by=owner.id) for i in range(23)])
            issue=CaseIssue(project_id="scope-project",kind="requirement",title="当前需求",created_by=owner.id,updated_by=owner.id)
            db.add(issue);db.flush()
            db.add_all([CaseIssueLink(case_id=f"scope-{i}",issue_id=issue.id,created_by=owner.id) for i in range(23)])
            review=create_review(db,owner,"scope-project",ReviewCreate(name="当前评审状态",caseIds=[f"scope-{i}" for i in range(23)],reviewerIds=[owner.id]))
            review_id=review.id
            from models.case_governance import CaseReviewItem
            item_id=db.query(CaseReviewItem).filter_by(review_id=review_id,case_id="scope-0").one().id
            db.commit()
        conditions=[
            ("优先级",{"priority":"P1"}),
            ("关注关系",{"followed":True}),
            ("附件关系",{"filters":{"conditions":[{"field":"attachment","operator":"contains","value":"当前附件"}]}}),
            ("需求关系",{"filters":{"conditions":[{"field":"requirementRef","operator":"contains","value":"当前需求"}]}}),
            ("评审状态",{"review_status":"pending"}),
        ]
        for label,condition in conditions:
            ready,proceed=threading.Event(),threading.Event()
            body=CaseBatchUpdate(selectAll=True,condition=condition,excludeIds=["scope-22"],tags=["回滚验收"])
            def waiting_writer():
                with Sessions() as db:
                    owner=db.get(User,"scope-owner")
                    assert preview(db,owner,"scope-project",body)["count"]==22
                    ready.set();assert proceed.wait(15)
                    result=batch_update(db,owner,"scope-project",body)
                    # 回滚此次批量写入，下一轮只检验另一关联条件。
                    db.rollback()
                    return result
            with ThreadPoolExecutor(max_workers=1) as pool:
                pending=pool.submit(waiting_writer)
                if not ready.wait(15):
                    pending.result(timeout=1)
                    raise RuntimeError("范围预览未就绪")
                try:
                    with Sessions() as holder:
                        owner=holder.get(User,"scope-owner");lock_project(holder,"scope-project")
                        if label=="优先级":holder.get(TestCase,"scope-0").priority="P0"
                        elif label=="关注关系":holder.query(CaseFollow).filter_by(case_id="scope-0").delete()
                        elif label=="附件关系":holder.query(CaseAttachment).filter_by(case_id="scope-0").delete()
                        elif label=="需求关系":holder.query(CaseIssueLink).filter_by(case_id="scope-0").delete()
                        else:vote_review(holder,owner,"scope-project",review_id,item_id,ReviewVote(decision="approved"))
                        holder.flush();proceed.set()
                        waited=False
                        for attempt in range(100):
                            waits=root_sql("SELECT COUNT(*) FROM performance_schema.data_lock_waits w JOIN performance_schema.data_locks l ON w.REQUESTING_ENGINE_LOCK_ID=l.ENGINE_LOCK_ID WHERE l.OBJECT_SCHEMA='"+name+"'")
                            if int(waits or 0):waited=True;break
                            time.sleep(0.05)
                        assert waited and not pending.done()
                        holder.commit()
                    assert pending.result(timeout=15)==21, label
                    if label=="优先级":
                        with Sessions() as restore:
                            restore.get(TestCase,"scope-0").priority="P1"
                            restore.commit()
                    log.info("%s验收通过：旧快照22，真实等待项目锁，提交后当前读21，跨页排除保留，批量写入回滚",label)
                finally:proceed.set()
        with Sessions() as db:
            assert db.query(TaskQueue).count()==0
            assert db.query(CaseVersion).count()==23
        print("真实MySQL五种范围当前读与回滚验收通过，零节点任务")
    except Exception:
        log.exception("真实MySQL范围验收失败")
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
