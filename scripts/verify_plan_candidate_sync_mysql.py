"""在独立临时MySQL库验证功能用例同步关联的锁内当前读和原子提交，不执行台架。"""

import json
import logging
from pathlib import Path
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
logging.basicConfig(
    filename=ROOT / "logs/第50部分MySQL验收.log",
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
    name = "ats_candidate_sync_" + uuid.uuid4().hex[:16]
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
        import threading
        import time
        from fastapi import HTTPException
        from models import TestPlan, PlanCaseRelation
        from models.case_features import CaseAutomationLink
        from schemas.plan_candidate_selection import Association
        from services.plan_candidate_selection import preview
        from services.plan_case_workspace import associate
        from services.review_workspace import lock_project
        with Sessions() as db:
            db.add(User(id='actor',username='同步关联验收',email='sync@example.test',password_hash='不登录'));db.flush()
            db.add_all([Project(id='a-target',name='目标计划项目',owner_id='actor'),Project(id='z-source',name='功能用例来源',owner_id='actor')]);db.flush()
            db.add(TestPlan(id='plan',project_id='a-target',owner_id='actor',name='同步计划',plan_number='SYNC'));db.flush()
            for identifier,kind in [('functional','functional'),('api-0','api'),('api-1','api')]:
                db.add(TestCase(id=identifier,project_id='z-source',name=identifier,case_code=identifier,type=kind,steps=[],is_automated=kind!='functional',created_by='actor'))
            db.flush();db.add(CaseAutomationLink(id='link',case_id='functional',target_case_id='api-0',category='api',created_by='actor'));db.commit()
        body=Association(projectId='z-source',caseIds=['functional'],syncCase=True,apiCaseCollectionId='default')
        for label in ['关联新增','关联撤销','目标回收','目标来源移动']:
            ready,proceed=threading.Event(),threading.Event()
            def writer():
                with Sessions() as db:
                    plan,actor=db.get(TestPlan,'plan'),db.get(User,'actor')
                    assert preview(db,plan,actor,body)['sync']['api']['count']==1
                    ready.set();assert proceed.wait(15)
                    try:
                        value=associate(db,plan,actor,body)
                        expected=2 if label=='关联新增' else 0
                        assert label!='目标来源移动' and value==dict(added=1,synced=dict(api=expected,scenario=0)),(label,value)
                    except HTTPException as exc:
                        log.exception('当前读拒绝失效来源：%s',label)
                        assert label=='目标来源移动' and exc.status_code==409
                    finally:db.rollback()
            with ThreadPoolExecutor(max_workers=1) as pool:
                pending=pool.submit(writer)
                if not ready.wait(15):pending.result(timeout=1);raise RuntimeError('同步预览未就绪')
                try:
                    with Sessions() as holder:
                        lock_project(holder,'z-source')
                        if label=='关联新增':holder.add(CaseAutomationLink(id='new',case_id='functional',target_case_id='api-1',category='api',created_by='actor'))
                        elif label=='关联撤销':holder.query(CaseAutomationLink).filter_by(id='link').delete()
                        elif label=='目标回收':holder.get(TestCase,'api-0').deleted_at=datetime.now()
                        else:holder.get(TestCase,'api-0').project_id='a-target'
                        holder.flush();proceed.set()
                        waited=False
                        for _ in range(100):
                            value=root_sql("SELECT COUNT(*) FROM performance_schema.data_lock_waits w JOIN performance_schema.data_locks l ON w.REQUESTING_ENGINE_LOCK_ID=l.ENGINE_LOCK_ID WHERE l.OBJECT_SCHEMA='"+name+"'")
                            if int(value or 0):waited=True;break
                            time.sleep(.05)
                        assert waited and not pending.done(),label
                        holder.commit()
                    pending.result(timeout=15)
                    log.info('%s通过：真实项目锁等待后重查功能关联及目标，写入回滚',label)
                finally:proceed.set()
            with Sessions() as db:
                db.get(TestCase,'api-0').deleted_at=None;db.get(TestCase,'api-0').project_id='z-source'
                db.query(CaseAutomationLink).delete();db.add(CaseAutomationLink(id='link',case_id='functional',target_case_id='api-0',category='api',created_by='actor'));db.commit()
        barrier=threading.Barrier(2)
        def concurrent():
            with Sessions() as db:
                actor,plan=db.get(User,'actor'),db.get(TestPlan,'plan')
                barrier.wait(timeout=10)
                value=associate(db,plan,actor,body);db.commit();return value
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures=[pool.submit(concurrent) for _ in range(2)]
            values=[f.result(timeout=20) for f in futures]
        assert sorted(v['added'] for v in values)==[0,1]
        assert sorted(v['synced']['api'] for v in values)==[0,1]
        with Sessions() as db:
            assert {r.case_id for r in db.query(PlanCaseRelation)}=={'functional','api-0'}
            assert db.query(PlanCaseRelation).count()==2
            assert db.query(TestCase).count()==3
            assert db.query(TaskQueue).count()==db.query(CaseVersion).count()==0
        log.info('并发同步提交通过：仅一次新增功能及接口关联，无重复/复制/版本/任务')
        print('真实MySQL通过：4项RR快照与锁等待当前读、并发同步单胜；未提交执行任务')
    finally:
        if engine is not None:engine.dispose()
        if granted:root_sql(f"REVOKE ALL PRIVILEGES ON `{name}`.* FROM {quote(account)}@{quote(host)}")
        if created:root_sql(f"DROP DATABASE `{name}`")
        log.info('独立临时库与临时授权已回收：%s',name)

if __name__=='__main__':
    try:main()
    except Exception:log.exception('同步关联真实MySQL验收失败');raise
