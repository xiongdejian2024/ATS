"""增量迁移保持历史数据、默认只预览、失败可重入。"""
import importlib.util
from pathlib import Path
from sqlalchemy import text, inspect
from database import engine

spec=importlib.util.spec_from_file_location('ats_workspace_upgrade',Path(__file__).resolve().parents[1]/'scripts/upgrade_ms_workspace.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)


def test_upgrade_preserves_old_review_and_is_idempotent():
    with engine.begin() as c:
        c.execute(text("INSERT INTO users (id,username,email,password_hash,status) VALUES ('owner','升级负责人','upgrade@example.test','仅测试',1)"))
        c.execute(text("INSERT INTO projects (id,name,owner_id,status) VALUES ('project','历史项目','owner','active')"))
        c.execute(text("INSERT INTO case_reviews (id,project_id,name,policy,reviewer_ids,status,created_by,description,mode) VALUES ('review','project','历史任一通过评审','any','[\"owner\"]','pending','owner','','multiple')"))
        for column in ['mode','description','parent_review_id','start_date','end_date']:
            c.execute(text(f'ALTER TABLE case_reviews DROP COLUMN {column}'))
        c.execute(text('DROP TABLE case_review_follows'))
    steps=module.upgrade(engine,False)
    assert steps and 'mode' not in {c['name'] for c in inspect(engine).get_columns('case_reviews')}
    module.upgrade(engine,True)
    with engine.connect() as c:
        assert c.execute(text("SELECT mode FROM case_reviews WHERE id='review'")).scalar()=='single'
        assert c.execute(text('SELECT COUNT(*) FROM case_reviews')).scalar()==1
        assert c.execute(text("SELECT name FROM projects WHERE id='project'")).scalar()=='历史项目'
    assert module.upgrade(engine,True)==[]


def test_migration_rejects_uninitialized_database(tmp_path):
    from sqlalchemy import create_engine
    import pytest
    empty=create_engine('sqlite:///'+str(tmp_path/'empty.sqlite'))
    with pytest.raises(RuntimeError,match='不是已初始化'):
        module.upgrade(empty,True)
    assert inspect(empty).get_table_names()==[]


def test_plan_collections_upgrade_preserves_legacy_relations_and_executor():
    with engine.begin() as connection:
        connection.execute(text("INSERT INTO users (id,username,email,password_hash,status) VALUES ('owner','原执行人','collection@example.com','仅测试',1)"))
        connection.execute(text("INSERT INTO projects (id,name,owner_id,status) VALUES ('project','旧计划项目','owner','active')"))
        connection.execute(text("INSERT INTO test_plans (id,project_id,owner_id,name,plan_number,plan_type,status) VALUES ('plan','project','owner','旧计划','TP-COLLECTION','manual','not_started')"))
        connection.execute(text("INSERT INTO test_cases (id,project_id,case_code,name,type,priority,steps,created_by,is_automated,status) VALUES ('case','project','OLD-COLLECTION','旧用例','functional','P2','[]','owner',0,'not_executed')"))
        connection.execute(text('DROP TABLE plan_case_relations'))
        connection.execute(text('CREATE TABLE plan_case_relations (id VARCHAR(36) PRIMARY KEY,plan_id VARCHAR(36) NOT NULL,case_id VARCHAR(36) NOT NULL,assigned_to VARCHAR(36),execution_order INTEGER NOT NULL DEFAULT 0,execution_status VARCHAR(50),execution_updated_at DATETIME,created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP)'))
        connection.execute(text("INSERT INTO plan_case_relations(id,plan_id,case_id,assigned_to,execution_status) VALUES ('relation','plan','case','owner','pass')"))
        connection.execute(text('ALTER TABLE plan_workspaces DROP COLUMN uses_tree'))
    preview=module.upgrade(engine,False)
    assert any('plan_case_relations.collection_id' in step[0] for step in preview)
    assert any('plan_workspaces.uses_tree' in step[0] for step in preview)
    module.upgrade(engine,True)
    with engine.connect() as connection:
        row=connection.execute(text("SELECT case_id,assigned_to,execution_status,collection_id FROM plan_case_relations WHERE id='relation'")).one()
        assert tuple(row)==('case','owner','pass',None)
    assert module.upgrade(engine,True)==[]


def test_execution_history_upgrade_preserves_runs_and_is_idempotent():
    """新历史表迁移不能删除或重写原计划报告。"""
    with engine.begin() as connection:
        connection.execute(text("INSERT INTO users (id,username,email,password_hash,status) VALUES ('owner','执行历史升级','execution-upgrade@example.com','仅测试',1)"))
        connection.execute(text("INSERT INTO projects (id,name,owner_id,status) VALUES ('project','执行历史旧项目','owner','active')"))
        connection.execute(text("INSERT INTO test_plans (id,project_id,owner_id,name,plan_number,plan_type,status) VALUES ('plan','project','owner','旧计划','TP-EXECUTION','manual','completed')"))
        connection.execute(text("INSERT INTO plan_runs (id,plan_id,executor_id,plan_name,status,config_snapshot,case_snapshot,manual_results,manual_revision,report) VALUES ('old-run','plan','owner','旧计划','completed','{}','[]','{}',0,:report)"), {'report':'{"total":1,"passed":1}'})
        connection.execute(text('DROP TABLE plan_case_executions'))
    preview=module.upgrade(engine,False)
    assert any('plan_case_executions' in description for description,_ in preview)
    assert 'plan_case_executions' not in inspect(engine).get_table_names()
    module.upgrade(engine,True)
    with engine.connect() as connection:
        assert connection.execute(text("SELECT report FROM plan_runs WHERE id='old-run'")).scalar()=='{"total":1,"passed":1}'
        assert connection.execute(text('SELECT COUNT(*) FROM plan_case_executions')).scalar()==0
    assert module.upgrade(engine,True)==[]


def test_review_time_columns_upgrade_keeps_legacy_dates_and_rows():
    with engine.begin() as connection:
        connection.execute(text("INSERT INTO users (id,username,email,password_hash,status) VALUES ('owner','周期升级','period@example.test','仅测试',1)"))
        connection.execute(text("INSERT INTO projects (id,name,owner_id,status) VALUES ('project','周期历史项目','owner','active')"))
        connection.execute(text("INSERT INTO case_reviews (id,project_id,name,policy,reviewer_ids,status,created_by,description,mode,start_date,end_date) VALUES ('review','project','历史周期','all','[\"owner\"]','pending','owner','','multiple','2026-10-05','2026-10-06')"))
        connection.execute(text("INSERT INTO review_workspaces (review_id,tags,archived) VALUES ('review','[\"旧标签\"]',0)"))
        connection.execute(text('ALTER TABLE review_workspaces DROP COLUMN start_time'))
        connection.execute(text('ALTER TABLE review_workspaces DROP COLUMN end_time'))
    preview=module.upgrade(engine,False)
    assert any('review_workspaces.start_time' in description for description,_ in preview)
    assert 'start_time' not in {column['name'] for column in inspect(engine).get_columns('review_workspaces')}
    module.upgrade(engine,True)
    with engine.connect() as connection:
        assert tuple(connection.execute(text("SELECT start_date,end_date,name FROM case_reviews WHERE id='review'")).one())==('2026-10-05','2026-10-06','历史周期')
        assert tuple(connection.execute(text("SELECT tags,start_time,end_time FROM review_workspaces WHERE review_id='review'")).one())==('["旧标签"]',None,None)
    assert module.upgrade(engine,True)==[]
