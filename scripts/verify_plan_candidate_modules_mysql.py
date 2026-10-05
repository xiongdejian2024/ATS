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
    filename=ROOT / "logs/第48部分MySQL验收.log",
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
    name = "ats_candidate_modules_" + uuid.uuid4().hex[:16]
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
        from datetime import datetime
        from fastapi import HTTPException
        from models import TestPlan, PlanCaseRelation, TestExecution, Module
        from models.plan_workspace import PlanWorkspace, PlanNode
        from schemas.plan_candidate_selection import Association
        from services.plan_candidate_selection import preview
        from services.plan_case_workspace import associate
        from services.review_workspace import lock_project
        from api.v1.case_governance import transact
        with Sessions() as db:
            owner = User(id="owner", username="范围验收", email="scope@example.test", password_hash="不登录")
            db.add(owner); db.flush()
            db.add(Project(id="project", name="独立范围验收", owner_id=owner.id)); db.flush()
            db.add_all([TestPlan(id=pid, project_id="project", owner_id="owner", name=pid, plan_number=pid) for pid in ["plan", "source"]]); db.flush()
            db.add(PlanWorkspace(plan_id="plan", uses_tree=False))
            db.add(Module(id="parent", project_id="project", name="父模块")); db.flush()
            db.add(Module(id="child", project_id="project", name="子模块", parent_id="parent")); db.flush()
            for i in range(23):
                db.add(TestCase(id=f"manual-{i}", project_id="project", name=f"手工范围{i}", case_code=f"MANUAL-{i}", type="functional", priority="P1", steps=[], module_id="child", is_automated=False, created_by="owner"))
            db.commit()
        full = lambda *ids: dict(selectAll=True, excludeIds=list(ids))
        with Sessions() as db:
            db.add(Module(id='sibling', project_id='project', name='另一个模块')); db.flush()
            for cid, mid in [('parent-case', 'parent'), ('side', 'sibling'), ('free', None)]:
                db.add(TestCase(id=cid, project_id='project', name=cid, case_code=cid, type='functional',
                    priority='P1', steps=[], module_id=mid, is_automated=False, created_by='owner'))
            db.commit()
        manual_scope = dict(moduleMaps=dict(parent=full(), child=full('manual-22'), sibling=dict(selectIds=['side'])))
        trials = [
            ('模块移动', manual_scope, 24, 23, None),
            ('用例回收', manual_scope, 24, 23, None),
            ('新增模块内用例', manual_scope, 24, 25, None),
            ('父子关系变化', manual_scope, 24, 24, None),
            ('逐条归属变化', dict(moduleMaps=dict(child=dict(selectIds=['manual-0']))), 1, 0, 409),
            ('已选模块删除', manual_scope, 24, 0, 404),
            ('全部模块子目录取消', dict(moduleMaps=dict(all=full(), child=dict(selectAll=False))), 3, 2, None),
        ]
        for label, payload, before, after, rejection in trials:
            ready, proceed = threading.Event(), threading.Event()
            body = Association(**payload)
            def waiting_writer():
                with Sessions() as db:
                    owner, plan = db.get(User, 'owner'), db.get(TestPlan, 'plan')
                    assert preview(db, plan, owner, body)['count'] == before
                    ready.set(); assert proceed.wait(15)
                    try:
                        result = associate(db, plan, owner, body)['added']
                        assert rejection is None
                    except HTTPException as exc:
                        log.exception('模块组合变化整批拒绝：%s', label)
                        assert exc.status_code == rejection
                        result = 0
                    finally: db.rollback()
                    return result
            with ThreadPoolExecutor(max_workers=1) as pool:
                pending = pool.submit(waiting_writer)
                if not ready.wait(15):
                    pending.result(timeout=1)
                    raise RuntimeError('模块范围预览未就绪')
                try:
                    with Sessions() as holder:
                        lock_project(holder, 'project')
                        if label == '模块移动' or label == '逐条归属变化': holder.get(TestCase, 'manual-0').module_id = 'sibling'
                        elif label == '用例回收': holder.get(TestCase, 'manual-0').deleted_at = datetime.now()
                        elif label == '新增模块内用例': holder.add(TestCase(id='late', project_id='project', name='新用例', case_code='LATE', type='functional', steps=[], module_id='child', is_automated=False, created_by='owner'))
                        elif label == '父子关系变化': holder.get(Module, 'child').parent_id = None
                        elif label == '已选模块删除':
                            holder.query(TestCase).filter_by(module_id='child').update({'module_id': None}); holder.delete(holder.get(Module, 'child'))
                        else: holder.get(TestCase, 'free').module_id = 'child'
                        holder.flush(); proceed.set()
                        waited = False
                        for _ in range(100):
                            waits = root_sql("SELECT COUNT(*) FROM performance_schema.data_lock_waits w JOIN performance_schema.data_locks l ON w.REQUESTING_ENGINE_LOCK_ID=l.ENGINE_LOCK_ID WHERE l.OBJECT_SCHEMA='" + name + "'")
                            if int(waits or 0): waited = True; break
                            time.sleep(.05)
                        assert waited and not pending.done(), label
                        holder.commit()
                    assert pending.result(timeout=15) == after, label
                    log.info('%s通过：旧预览%s，实际等待项目锁，锁内当前范围%s，整批回滚', label, before, after)
                finally: proceed.set()
            with Sessions() as restore:
                if not restore.get(Module, 'child'):
                    restore.add(Module(id='child', project_id='project', name='子模块', parent_id='parent')); restore.flush()
                restore.get(Module, 'child').parent_id = 'parent'
                for i in range(23):
                    row = restore.get(TestCase, f'manual-{i}'); row.module_id = 'child'; row.deleted_at = None
                restore.get(TestCase, 'free').module_id = None
                restore.query(TestCase).filter_by(id='late').delete(); restore.commit()
                assert restore.query(PlanCaseRelation).filter_by(plan_id='plan').count() == 0
        def competing(index):
            with Sessions() as db:
                try:
                    transact(db, lambda: associate(db, db.get(TestPlan, 'plan'), db.get(User, 'owner'), Association(**manual_scope)))
                    return 200
                except HTTPException as exc:
                    log.exception('模块组合并发单胜：另一请求拒绝')
                    return exc.status_code
        with ThreadPoolExecutor(max_workers=2) as pool:
            assert sorted(pool.map(competing, [0, 1])) == [200, 409]
        with Sessions() as db:
            actual = {row.case_id for row in db.query(PlanCaseRelation).filter_by(plan_id='plan')}
            assert actual == {'parent-case', 'side'} | {f'manual-{i}' for i in range(22)}
            assert db.query(CaseVersion).count() == db.query(TaskQueue).count() == 0
        log.info('并发单胜200/409，实际24条关系，重复0、版本0、节点任务0')
        print('真实MySQL七种模块组合当前读和并发单胜验收通过；未运行台架')
    except Exception:
        log.exception("真实MySQL模块组合验收失败")
        raise
    finally:
        if engine is not None:engine.dispose()
        if granted:root_sql(f"REVOKE ALL PRIVILEGES ON `{name}`.* FROM {quote(account)}@{quote(host)}")
        if created:root_sql(f"DROP DATABASE `{name}`")
        log.info("独立临时库与临时授权已回收：%s",name)

if __name__=="__main__":main()
