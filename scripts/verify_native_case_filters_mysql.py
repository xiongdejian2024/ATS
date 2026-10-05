"""在独立临时MySQL库验证原生参数、执行结果和并发版本，不执行台架。"""

import json
import logging
from pathlib import Path
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
logging.basicConfig(
    filename=ROOT / "logs/第46部分MySQL验收.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("原生配置数据库验收")


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
    name = "ats_native_filter_" + uuid.uuid4().hex[:16]
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
        from models import TestPlan, TestExecution
        from models.native_case import ApiDefinition, NativeCaseConfig
        from schemas.native_case import DefinitionInput, ConfigInput
        from services.native_case import save_entity, save_config, config_data
        from services.plan_candidate_filter import advanced_candidates
        from api.v1.case_governance import transact
        from datetime import datetime
        with Sessions() as db:
            owner=User(id="owner",username="原生配置验收",email="native@example.test",password_hash="不登录")
            db.add(owner);db.flush()
            db.add(Project(id="project",name="独立原生验收",owner_id=owner.id));db.flush()
            plan=TestPlan(id="plan",project_id="project",owner_id="owner",name="独立计划",plan_number="QA46")
            db.add(plan);db.flush()
            case=TestCase(id="case",project_id="project",name="原生用例",case_code="QA46-CASE",type="api",steps=[],created_by="owner",is_automated=True,status="failed")
            db.add(case);db.flush()
            data=save_entity(db,owner,"project",ApiDefinition,DefinitionInput(name="接口",protocol="HTTP",path="/诊断",parameters={"enabled":False,"count":0}))
            definition=data['definitions'][0]
            save_config(db,owner,"project","case",ConfigInput(state="PROCESSING",apiDefinitionId=definition['id'],expectedDefinitionRevision=1,parameters=definition['parameters']))
            db.add(TestExecution(id="report",case_id="case",executor_id="owner",result="passed",executed_at=datetime(2026,10,6)))
            db.commit()
            definition_id=definition['id']
            data=save_entity(db,owner,"project",ApiDefinition,DefinitionInput(name="接口",protocol="HTTP",path="/诊断",parameters={"enabled":0,"count":False},expectedRevision=1),definition_id)
            db.commit()
            assert config_data(db,owner,"project","case")['apiChange']
            assert type(db.get(ApiDefinition,definition_id).parameters['enabled']) is int
            query={"conditions":[{"field":"apiChange","operator":"equals","value":True},{"field":"lastReportStatus","operator":"equals","value":"SUCCESS"}],"logic":"and"}
            assert advanced_candidates(db,plan,"api",query,False,"owner",1,20)['total']==1
        def update_profile(index):
            with Sessions() as db:
                try:
                    transact(db,lambda:save_config(db,db.get(User,"owner"),"project","case",ConfigInput(state="DONE",apiDefinitionId=definition_id,expectedDefinitionRevision=2,expectedRevision=1,parameters={"enabled":0,"count":False},syncDefinition=True)))
                    return 200
                except HTTPException as exc:
                    return exc.status_code
        with ThreadPoolExecutor(max_workers=2) as pool:
            assert sorted(pool.map(update_profile,[0,1]))==[200,409]
        with Sessions() as db:
            assert not config_data(db,db.get(User,"owner"),"project","case")['apiChange']
            assert db.get(NativeCaseConfig,"case").revision==2
            assert type(db.get(NativeCaseConfig,"case").parameters['enabled']) is int
            assert db.query(CaseVersion).count()==3
            assert db.query(TaskQueue).count()==0
        log.info("真实MySQL原生JSON布尔与数字区分、版本留存、参数变更、实际执行记录筛选及并发单胜通过")
        print("真实MySQL：原生配置、真实结果筛选及并发单胜通过；活动任务0")
    except Exception:
        log.exception("真实MySQL原生配置验收失败")
        raise
    finally:
        if engine is not None:engine.dispose()
        if granted:root_sql(f"REVOKE ALL PRIVILEGES ON `{name}`.* FROM {quote(account)}@{quote(host)}")
        if created:root_sql(f"DROP DATABASE `{name}`")
        log.info("独立临时库与临时授权已回收：%s",name)

if __name__=="__main__":main()
