"""在独立临时MySQL库验证多模块关联锁内当前读和并发提交，不执行台架。"""

import json
import logging
from pathlib import Path
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
logging.basicConfig(
    filename=ROOT / "logs/第49部分MySQL验收.log",
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
    name = "ats_candidate_projects_" + uuid.uuid4().hex[:16]
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
        from fastapi import HTTPException
        from models import TestPlan, PlanCaseRelation, ProjectMember, Permission, ProjectPermission, Role, RolePermission, UserRole
        from models.plan_workspace import PlanWorkspace
        from schemas.plan_candidate_selection import Association
        from services.plan_candidate_selection import preview
        from services.plan_case_workspace import associate
        from services.review_workspace import lock_project
        with Sessions() as db:
            db.add_all([User(id="actor",username="跨项目验收",email="actor@example.test",password_hash="不登录"), User(id="other",username="来源所有者",email="other@example.test",password_hash="不登录")]);db.flush()
            db.add_all([Project(id="a-target",name="目标",owner_id="actor"),Project(id="z-source",name="来源",owner_id="other")]);db.flush()
            db.add(ProjectMember(project_id="z-source",user_id="actor",role="member"))
            db.add_all([TestPlan(id="plan",project_id="a-target",owner_id="actor",name="目标计划",plan_number="TARGET"), TestPlan(id="reverse",project_id="z-source",owner_id="actor",name="反向计划",plan_number="SOURCE")]);db.flush()
            db.add_all([TestCase(id=f"foreign-{i}",project_id="z-source",name=f"来源{i}",case_code=f"SOURCE-{i}",type="functional",steps=[],created_by="actor") for i in range(3)])
            db.add(TestCase(id="target-case",project_id="a-target",name="目标用例",case_code="TARGET",type="functional",steps=[],created_by="actor"))
            db.add(Permission(id="read",code="test_case:read",name="读取用例",resource="test_case",action="read"))
            db.add(Role(id="role",name="验收角色",display_name="验收角色"));db.commit()
        labels=["来源成员撤权","来源所有者撤权","项目权限撤权","全局角色权限撤权","用户停用","目标权限撤权","来源用例移动","来源新增用例"]
        for label in labels:
            with Sessions() as setup:
                if label != "来源成员撤权": setup.query(ProjectMember).filter_by(project_id="z-source",user_id="actor").delete()
                if label in {"来源所有者撤权","用户停用","目标权限撤权","来源用例移动","来源新增用例"}: setup.get(Project,"z-source").owner_id="actor"
                if label == "项目权限撤权": setup.add(ProjectPermission(project_id="z-source",user_id="actor",permission_id="read"))
                if label == "全局角色权限撤权":
                    setup.add(UserRole(user_id="actor",role_id="role"));setup.add(RolePermission(role_id="role",permission_id="read"))
                setup.commit()
            ready, proceed=threading.Event(),threading.Event()
            body=Association(projectId="z-source",selectAll=True)
            def writer():
                with Sessions() as db:
                    actor, plan=db.get(User,"actor"),db.get(TestPlan,"plan")
                    assert preview(db,plan,actor,body)["count"]==3
                    ready.set();assert proceed.wait(15)
                    try:
                        value=associate(db,plan,actor,body)["added"]
                        expected=2 if label == "来源用例移动" else 4
                        assert label in {"来源用例移动","来源新增用例"} and value==expected,(label,value)
                    except HTTPException as exc:
                        log.exception("锁等待后按最新权限拒绝关联：%s",label)
                        assert label not in {"来源用例移动","来源新增用例"} and exc.status_code==403,(label,exc.status_code)
                    finally: db.rollback()
            with ThreadPoolExecutor(max_workers=1) as pool:
                pending=pool.submit(writer)
                if not ready.wait(15): pending.result(timeout=1);raise RuntimeError("预览未就绪")
                try:
                    with Sessions() as holder:
                        lock_project(holder,"a-target" if label == "目标权限撤权" else "z-source")
                        if label == "来源成员撤权": holder.query(ProjectMember).filter_by(project_id="z-source",user_id="actor").delete()
                        elif label == "来源所有者撤权": holder.get(Project,"z-source").owner_id="other"
                        elif label == "项目权限撤权": holder.query(ProjectPermission).filter_by(project_id="z-source",user_id="actor").delete()
                        elif label == "全局角色权限撤权": holder.query(RolePermission).filter_by(role_id="role").delete()
                        elif label == "用户停用": holder.get(User,"actor").status=False
                        elif label == "目标权限撤权": holder.get(Project,"a-target").owner_id="other"
                        elif label == "来源用例移动": holder.get(TestCase,"foreign-0").project_id="a-target"
                        else: holder.add(TestCase(id="new",project_id="z-source",name="新来源",case_code="NEW",type="functional",steps=[],created_by="actor"))
                        holder.flush();proceed.set()
                        waited=False
                        for _ in range(100):
                            waits=root_sql("SELECT COUNT(*) FROM performance_schema.data_lock_waits w JOIN performance_schema.data_locks l ON w.REQUESTING_ENGINE_LOCK_ID=l.ENGINE_LOCK_ID WHERE l.OBJECT_SCHEMA='"+name+"'")
                            if int(waits or 0):waited=True;break
                            time.sleep(.05)
                        assert waited and not pending.done(),label
                        holder.commit()
                    pending.result(timeout=15)
                    log.info("%s通过：真实锁等待，旧快照不可授权新写入，写入全部回滚",label)
                finally:proceed.set()
            with Sessions() as restore:
                restore.get(User,"actor").status=True;restore.get(Project,"a-target").owner_id="actor";restore.get(Project,"z-source").owner_id="other"
                restore.get(TestCase,"foreign-0").project_id="z-source"
                restore.query(TestCase).filter_by(id="new").delete()
                restore.query(ProjectPermission).delete();restore.query(RolePermission).delete();restore.query(UserRole).delete();restore.query(ProjectMember).delete()
                restore.add(ProjectMember(project_id="z-source",user_id="actor",role="member"));restore.commit()
        with Sessions() as setup:setup.get(Project,"z-source").owner_id="actor";setup.commit()
        barrier=threading.Barrier(2)
        def direction(plan_id,source):
            with Sessions() as db:
                plan,actor=db.get(TestPlan,plan_id),db.get(User,"actor")
                barrier.wait(timeout=10)
                result=associate(db,plan,actor,Association(projectId=source,selectAll=True))["added"]
                db.commit();return result
        with ThreadPoolExecutor(max_workers=2) as pool:
            first=pool.submit(direction,"plan","z-source");second=pool.submit(direction,"reverse","a-target")
            assert (first.result(timeout=20),second.result(timeout=20))==(3,1)
        with Sessions() as db:
            assert db.query(PlanCaseRelation).count()==4
            assert db.query(TaskQueue).count()==db.query(CaseVersion).count()==0
            assert db.query(TestCase).count()==4
        log.info("双向跨项目并发关联通过：按项目ID统一锁顺序，保留四个主用例，无任务或复制")
        # 在预先建立 RR 快照后撤销来源权限，手工计划也不能冻结未授权版本。
        from services.plan_orchestration import start_plan_run
        import asyncio
        ready, proceed=threading.Event(),threading.Event()
        def waiting_run():
            with Sessions() as db:
                assert db.get(Project,"z-source").owner_id=="actor"
                assert db.query(ProjectMember).filter_by(project_id="z-source",user_id="actor").count()==1
                ready.set();assert proceed.wait(15)
                try:
                    asyncio.run(start_plan_run(db,"plan","actor",commit=False))
                    raise AssertionError("来源撤权后不应冻结执行版本")
                except HTTPException as exc:
                    log.exception("执行冻结按锁内最新来源权限拒绝")
                    assert exc.status_code==403
                finally:db.rollback()
        with ThreadPoolExecutor(max_workers=1) as pool:
            pending=pool.submit(waiting_run)
            if not ready.wait(15):pending.result(timeout=1);raise RuntimeError("执行旧快照未就绪")
            try:
                with Sessions() as holder:
                    lock_project(holder,"z-source")
                    holder.get(Project,"z-source").owner_id="other"
                    holder.query(ProjectMember).filter_by(project_id="z-source",user_id="actor").delete()
                    holder.flush();proceed.set()
                    waited=False
                    for _ in range(100):
                        waits=root_sql("SELECT COUNT(*) FROM performance_schema.data_lock_waits w JOIN performance_schema.data_locks l ON w.REQUESTING_ENGINE_LOCK_ID=l.ENGINE_LOCK_ID WHERE l.OBJECT_SCHEMA='"+name+"'")
                        if int(waits or 0):waited=True;break
                        time.sleep(.05)
                    assert waited and not pending.done()
                    holder.commit()
                pending.result(timeout=15)
            finally:proceed.set()
        with Sessions() as db:
            from models.plan_orchestration import PlanRun
            assert db.query(TaskQueue).count()==db.query(CaseVersion).count()==db.query(PlanRun).count()==0
        log.info("执行冻结旧快照撤权验证通过：真实锁等待、HTTP403、无冻结版本/批次/任务")

        print("真实MySQL通过：8项关联及1项执行冻结撤权/当前读，双向并发无死锁；全部临时库清理")
    finally:
        if engine is not None:engine.dispose()
        if granted:root_sql(f"REVOKE ALL PRIVILEGES ON `{name}`.* FROM {quote(account)}@{quote(host)}")
        if created:root_sql(f"DROP DATABASE `{name}`")
        log.info("独立临时库与临时授权已回收：%s",name)

if __name__=="__main__":
    try: main()
    except Exception:
        log.exception("跨项目真实MySQL验收失败")
        raise
