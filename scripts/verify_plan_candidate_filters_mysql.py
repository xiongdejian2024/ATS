"""在独立临时MySQL库验证关联筛选及个人视图并发上限，不执行台架。"""

import json
import logging
from pathlib import Path
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
logging.basicConfig(
    filename=ROOT / "logs/第45部分MySQL验收.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("计划筛选数据库验收")


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
    name = "ats_candidate_filter_" + uuid.uuid4().hex[:16]
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
        from fastapi import HTTPException
        from models import TestPlan, PlanCaseRelation
        from models.plan_case_view import PlanCaseSavedView
        from models.plan_workspace import PlanWorkspace
        from schemas.plan_candidate_view import CandidateViewCreate
        from services.plan_candidate_filter import advanced_candidates, plan_membership
        from services.plan_case_view import save
        from api.v1.case_governance import transact
        with Sessions() as db:
            owner=User(id="owner",username="关联验收",email="candidate@example.test",password_hash="不登录")
            db.add(owner);db.flush()
            db.add(Project(id="project",name="独立关联验收",owner_id=owner.id));db.flush()
            plan=TestPlan(id="plan",project_id="project",owner_id="owner",name="独立计划",plan_number="QA45")
            db.add(plan);db.flush()
            case=TestCase(id="case",project_id="project",name="主用例结果",case_code="QA45-CASE",type="functional",steps=[],created_by="owner",is_automated=False,status="failed")
            db.add(case);db.flush()
            db.add(PlanCaseRelation(plan_id="plan",case_id="case"))
            for i in range(9):
                save(db,owner,plan,"functional-drawer",CandidateViewCreate(name=f"个人视图{i}",filters={}))
            save(db,owner,plan,"functional",CandidateViewCreate(name="个人视图0",filters={}))
            db.commit()
            filters={"conditions":[{"field":"status","operator":"equals","value":"failed"},{"field":"planIds","operator":"equals","value":"plan"}],"logic":"and"}
            assert advanced_candidates(db,plan,"functional",filters,True,"owner",1,20)["total"]==1
            db.add(PlanWorkspace(plan_id="plan",uses_tree=True));db.commit()
            assert not plan_membership(db,"project")[0]
            assert advanced_candidates(db,plan,"functional",filters,False,"owner",1,20)["total"]==0
            assert db.query(CaseVersion).count()==0 and db.query(TaskQueue).count()==0
        def concurrent_create(index):
            with Sessions() as db:
                try:
                    transact(db,lambda:save(db,db.get(User,"owner"),db.get(TestPlan,"plan"),"functional-drawer",CandidateViewCreate(name=f"并发{index}",filters={})))
                    return 200
                except HTTPException as exc:
                    return exc.status_code
        with ThreadPoolExecutor(max_workers=2) as pool:
            assert sorted(pool.map(concurrent_create,[0,1]))==[200,409]
        with Sessions() as db:
            assert db.query(PlanCaseSavedView).filter_by(category="functional-drawer").count()==10
            for category in ["api-drawer","scenario-drawer"]:
                save(db,db.get(User,"owner"),db.get(TestPlan,"plan"),category,CandidateViewCreate(name="个人视图0",filters={}))
            db.commit()
            try:
                transact(db,lambda:save(db,db.get(User,"owner"),db.get(TestPlan,"plan"),"api-drawer",CandidateViewCreate(name="个人视图0",filters={})))
            except HTTPException as exc:
                assert exc.status_code==409
            else:raise AssertionError("同名视图应被唯一约束拒绝")
            assert db.query(PlanCaseSavedView).count()==13 and db.query(TaskQueue).count()==0
        log.info("真实MySQL已验证主用例结果/有效计划关系/空树旧关系屏蔽、分类和工作区隔离、并发10个上限及唯一约束回滚")
        print("真实MySQL：主用例筛选、有效计划关系、视图隔离和并发上限通过；活动任务0")
    except Exception:
        log.exception("真实MySQL计划筛选验收失败")
        raise
    finally:
        if engine is not None:engine.dispose()
        if granted:root_sql(f"REVOKE ALL PRIVILEGES ON `{name}`.* FROM {quote(account)}@{quote(host)}")
        if created:root_sql(f"DROP DATABASE `{name}`")
        log.info("独立临时库与临时授权已回收：%s",name)

if __name__=="__main__":main()
