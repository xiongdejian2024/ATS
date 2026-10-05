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
    filename=ROOT / "logs/第53部分MySQL验收.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("原生计划实例范围数据库验收")


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
    name = "ats_native_scope_" + uuid.uuid4().hex[:16]
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
        from datetime import datetime
        import threading, time
        from fastapi import HTTPException
        from models import TestPlan, TestSuite, PlanCaseRelation, Module, Environment
        from models.plan_workspace import PlanWorkspace
        from models.plan_orchestration import PlanRun
        from models.native_case import ApiDefinition, NativeCaseConfig, ApiTestEnvironment
        from schemas.plan_native_selection import NativeWorkspaceBatch
        from services.plan_native_selection import preview, apply
        from services.review_workspace import lock_project
        from api.v1.case_governance import transact
        steps=[dict(action="原步骤",expected="已保存")]
        with Sessions() as db:
            db.add(User(id="owner",username="范围验收",email="native@example.test",password_hash="不登录"));db.flush()
            db.add(Project(id="project",name="独立原生范围验收",owner_id="owner"));db.flush()
            db.add(TestPlan(id="plan",project_id="project",owner_id="owner",name="隔离范围计划",plan_number="NATIVE"));db.flush()
            db.add(PlanWorkspace(plan_id="plan",uses_tree=False))
            db.add(Module(id="parent",project_id="project",name="父模块"));db.flush()
            db.add(Module(id="child",project_id="project",name="子模块",parent_id="parent"))
            db.add(Environment(id="offline",name="绝不执行",is_online=False))
            db.add(ApiDefinition(id="definition",project_id="project",name="定义",protocol="HTTP",path="/隔离接口",parameters={},updated_by="owner"))
            db.add(ApiTestEnvironment(id="env",project_id="project",name="原生配置环境",address="不发送网络请求",updated_by="owner"));db.flush()
            for category in ["api","scenario"]:
                for i in range(3):
                    cid=f"{category}-{i}"
                    db.add(TestCase(id=cid,project_id="project",module_id="child",case_code=cid,name=cid,type=category,is_automated=True,priority="P1",steps=steps,created_by="owner"));db.flush()
                    db.add(NativeCaseConfig(case_id=cid,state="PROCESSING" if category=="api" else "UNDERWAY",api_definition_id="definition" if category=="api" else None,environment_id="env",parameters={},updated_by="owner"))
                    db.add(PlanCaseRelation(id=f"relation-{cid}",plan_id="plan",case_id=cid,execution_order=i))
            db.add(TestSuite(id="suite",plan_id="plan",name="隔离模板",environment_id="offline",execution_command="不会执行",case_ids=["api-0"],created_by="owner"))
            db.add(PlanRun(id="history",plan_id="plan",plan_name="冻结报告",executor_id="owner",status="completed",config_snapshot={},case_snapshot=[],manual_results={},report={"cases":[dict(caseId=f"api-{i}",associationId=f"api-{i}",result="passed") for i in range(3)]}));db.commit()
        c=lambda field,operator,value:dict(field=field,operator=operator,value=value)
        def scope(category="api",**condition):
            return dict(category=category,selectAll=True,excludeIds=[f"legacy:relation-{category}-2:{category}-2"],condition=condition,action="unlink")
        trials=[
            ("优先级",scope(priority="P1"),1),
            ("模块层级",scope(tree_type="MODULE",folder="parent"),0),
            ("协议",scope(protocols="HTTP"),0),
            ("原生状态",scope(filters=dict(conditions=[c("nativeState","equals","PROCESSING")])),1),
            ("配置环境",scope(filters=dict(conditions=[c("environmentName","equals","env")])),1),
            ("实例最新结果",scope(result="SUCCESS"),1),
            ("场景步骤数",scope("scenario",filters=dict(conditions=[c("stepTotal","equals",1)])),1),
            ("新关联实例",scope(),3),
            ("活动测试套",scope(),0),
            ("归档状态",scope(),0),
        ]
        for label,payload,expected in trials:
            ready,proceed=threading.Event(),threading.Event();body=NativeWorkspaceBatch(**payload)
            def writer():
                with Sessions() as db:
                    owner,plan=db.get(User,"owner"),db.get(TestPlan,"plan")
                    assert preview(db,plan,owner,body)["count"]==2
                    ready.set();assert proceed.wait(15)
                    try:count=apply(db,plan,owner,body)["updated"]
                    except HTTPException as exc:
                        log.exception("预期范围为空、活动测试套或归档拒绝：%s",label)
                        assert exc.status_code==409;count=0
                    finally:db.rollback()
                    return count
            with ThreadPoolExecutor(max_workers=1) as pool:
                pending=pool.submit(writer)
                if not ready.wait(15):pending.result(timeout=1);raise RuntimeError("原生范围预览未就绪")
                try:
                    with Sessions() as holder:
                        lock_project(holder,"project")
                        if label=="优先级":holder.get(TestCase,"api-0").priority="P0"
                        elif label=="模块层级":holder.get(Module,"child").parent_id=None
                        elif label=="协议":holder.get(ApiDefinition,"definition").protocol="TCP"
                        elif label=="原生状态":holder.get(NativeCaseConfig,"api-0").state="DONE"
                        elif label=="配置环境":holder.get(NativeCaseConfig,"api-0").environment_id=None
                        elif label=="实例最新结果":holder.add(PlanRun(id="later",plan_id="plan",plan_name="更新冻结报告",executor_id="owner",created_at=datetime(2030,1,1),status="completed",config_snapshot={},case_snapshot=[],manual_results={},report={"cases":[dict(caseId="api-0",associationId="api-0",result="failed")]}))
                        elif label=="场景步骤数":holder.get(TestCase,"scenario-0").steps=steps*2
                        elif label=="新关联实例":holder.add(PlanCaseRelation(id="new-instance",plan_id="plan",case_id="api-0",execution_order=4))
                        elif label=="活动测试套":holder.add(TaskQueue(id="active",environment_id="offline",suite_id="suite",execution_id="不会执行",executor_id="owner",status="running"))
                        else:holder.get(PlanWorkspace,"plan").archived=True
                        holder.flush();proceed.set()
                        waited=False
                        for _ in range(100):
                            waits=root_sql("SELECT COUNT(*) FROM performance_schema.data_lock_waits w JOIN performance_schema.data_locks l ON w.REQUESTING_ENGINE_LOCK_ID=l.ENGINE_LOCK_ID WHERE l.OBJECT_SCHEMA='"+name+"'")
                            if int(waits or 0):waited=True;break
                            time.sleep(.05)
                        assert waited and not pending.done(),label
                        holder.commit()
                    assert pending.result(timeout=15)==expected,label
                    log.info("%s通过：旧预览2、真实项目锁等待、锁内实际范围%s；操作回滚，跨页排除保持",label,expected)
                finally:proceed.set()
            with Sessions() as restore:
                restore.get(TestCase,"api-0").priority="P1";restore.get(Module,"child").parent_id="parent"
                restore.get(ApiDefinition,"definition").protocol="HTTP"
                cfg=restore.get(NativeCaseConfig,"api-0");cfg.state="PROCESSING";cfg.environment_id="env"
                restore.get(TestCase,"scenario-0").steps=steps;restore.get(PlanWorkspace,"plan").archived=False
                restore.query(PlanRun).filter_by(id="later").delete();restore.query(PlanCaseRelation).filter_by(id="new-instance").delete();restore.query(TaskQueue).filter_by(id="active").delete();restore.commit()
                assert restore.query(PlanCaseRelation).count()==6 and restore.query(TaskQueue).count()==0
        def concurrent(index):
            with Sessions() as db:
                try:transact(db,lambda:apply(db,db.get(TestPlan,"plan"),db.get(User,"owner"),NativeWorkspaceBatch(**scope())));return 200
                except HTTPException as exc:return exc.status_code
        with ThreadPoolExecutor(max_workers=2) as pool:assert sorted(pool.map(concurrent,[0,1]))==[200,409]
        with Sessions() as db:
            assert {r.case_id for r in db.query(PlanCaseRelation).filter(PlanCaseRelation.case_id.like("api-%"))}=={"api-2"}
            assert db.query(TestCase).count()==6 and db.query(CaseVersion).count()==0 and db.query(TaskQueue).count()==0
        log.info("并发取消单胜200/409，仅排除实例保留；主用例6、版本0、执行队列0")
        print("真实MySQL十种原生范围当前读及并发取消通过；未执行台架")
    except Exception:
        log.exception("真实MySQL原生实例范围验收失败")
        raise
    finally:
        if engine is not None:engine.dispose()
        if granted:root_sql(f"REVOKE ALL PRIVILEGES ON `{name}`.* FROM {quote(account)}@{quote(host)}")
        if created:root_sql(f"DROP DATABASE `{name}`")
        log.info("独立临时库与临时授权已回收：%s",name)

if __name__=="__main__":main()
