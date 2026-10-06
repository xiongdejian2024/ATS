"""在独立临时MySQL库验证实例缺陷迁移、幂等与并发绑定，不执行台架。"""

import json
import logging
from pathlib import Path
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
logging.basicConfig(
    filename=ROOT / "logs/第75部分MySQL验收.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("计划实例缺陷数据库验收")


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
    name = "ats_defect_binding_" + uuid.uuid4().hex[:16]
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
        from models import TestPlan, PlanCaseRelation
        from models.case_features import CaseIssue
        from models.plan_case_defect import PlanCaseDefect
        from schemas.plan_case_defect import PlanDefectCreate, PlanDefectAssociate
        from services.plan_case_defect import create, associate
        from sqlalchemy import inspect
        from upgrade_plan_case_defects import upgrade
        table = PlanCaseDefect.__table__
        table.drop(engine)
        assert upgrade(False, engine) == ['plan_case_defects']
        assert upgrade(True, engine) == ['plan_case_defects']
        assert upgrade(True, engine) == []
        log.info('真实MySQL新表迁移、字段、唯一约束、外键与索引校验幂等通过')
        with Sessions() as db:
            db.add(User(id='owner', username='缺陷验收', email='defect@example.test', password_hash='不登录')); db.flush()
            db.add(Project(id='project', name='临时缺陷项目', owner_id='owner')); db.flush()
            db.add(TestPlan(id='plan', project_id='project', owner_id='owner', name='缺陷计划', plan_number='DEFECT')); db.flush()
            db.add(TestCase(id='case', project_id='project', case_code='CASE', name='功能用例😀', type='functional', steps=[], is_automated=False, created_by='owner')); db.flush()
            db.add(PlanCaseRelation(id='relation', plan_id='plan', case_id='case')); db.commit()
        scope = dict(selectIds=['legacy:relation:case'])
        request = PlanDefectCreate(**scope, requestId=str(uuid.uuid4()), title='并发同一新建缺陷😀', description='中文持久化')
        def submit():
            with Sessions() as db:
                try:
                    result = create(db, db.get(TestPlan,'plan'), db.get(User,'owner'), request)
                    db.commit(); return result
                except Exception:
                    log.exception('并发新建计划缺陷失败'); db.rollback(); raise
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(submit) for _ in range(2)]
            results = [f.result(timeout=30) for f in futures]
        assert results[0]['issueId'] == results[1]['issueId']
        assert sorted(r['replayed'] for r in results) == [False, True]
        with Sessions() as db:
            assert db.query(CaseIssue).count() == db.query(PlanCaseDefect).count() == 1
            assert db.query(CaseIssue).one().title.endswith('😀')
            db.add(CaseIssue(id='existing', project_id='project',kind='defect',title='既有缺陷',created_by='owner',updated_by='owner')); db.commit()
        data = PlanDefectAssociate(**scope, issueIds=['existing'])
        def attach():
            with Sessions() as db:
                try:
                    result=associate(db,db.get(TestPlan,'plan'),db.get(User,'owner'),data);db.commit();return result['updated']
                except Exception:
                    log.exception('并发关联既有缺陷失败');db.rollback();raise
        with ThreadPoolExecutor(max_workers=2) as pool:
            results=[f.result(timeout=30) for f in [pool.submit(attach) for _ in range(2)]]
        assert sorted(results)==[0,1]
        with Sessions() as db:
            assert db.query(PlanCaseDefect).count()==2 and db.query(TaskQueue).count()==0
        log.info('真实MySQL并发同请求仅创建1缺陷与1关系，并发既有缺陷仅新增1关系，中文快照保持，节点任务0')
        print('真实MySQL实例缺陷迁移与并发绑定通过，独立临时库完成回收')
    except Exception:
        log.exception("真实MySQL计划实例缺陷验收失败")
        raise
    finally:
        if engine is not None:engine.dispose()
        if granted:root_sql(f"REVOKE ALL PRIVILEGES ON `{name}`.* FROM {quote(account)}@{quote(host)}")
        if created:root_sql(f"DROP DATABASE `{name}`")
        log.info("独立临时库与临时授权已回收：%s",name)

if __name__=="__main__":main()
