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
