"""复用临时MySQL验收夹具验证功能日志尾部投影；不改正式库。"""
import importlib.util
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'backend'))
sys.path.insert(0,str(ROOT/'scripts'))
logging.basicConfig(filename=ROOT/'logs/第72部分MySQL验收.log',level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger('功能日志MySQL验收')


def verify(db):
    from models.test_suite import TestSuiteLog
    from services.bounded_logs import log_window
    from sqlalchemy import text as sql_text
    from upgrade_functional_log_storage import upgrade
    original = '迁移前中文😀日志'
    db.add(TestSuiteLog(id='migration-original',suite_id='suite',execution_id='old',message=original));db.commit()
    with db.bind.begin() as connection:
        connection.execute(sql_text("ALTER TABLE test_suite_logs MODIFY COLUMN message TEXT COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '保留原日志说明'"))
    assert upgrade(False, db.bind) == ['test_suite_logs.message']
    assert upgrade(True, db.bind) == ['test_suite_logs.message']
    assert upgrade(True, db.bind) == []
    from sqlalchemy import inspect
    migrated = next(c for c in inspect(db.bind).get_columns('test_suite_logs') if c['name']=='message')
    assert migrated['type'].collation == 'utf8mb4_unicode_ci' and migrated['comment'] == '保留原日志说明'
    assert db.query(TestSuiteLog.message).filter_by(id='migration-original').scalar() == original
    db.query(TestSuiteLog).filter_by(id='migration-original').delete();db.commit()
    log.info('旧TEXT升级LONGTEXT两次幂等，原中文emoji正文不变')
    text = '功能前段' * 100000 + '\n中文😀末尾'
    for i in range(25):
        db.add(TestSuiteLog(id=f'log-{i:02d}', suite_id='suite', execution_id=f'run-{i}', message=text,
                            timestamp=datetime(2026,10,6)+timedelta(seconds=i)))
    db.commit()
    query = db.query(TestSuiteLog).filter_by(suite_id='suite')
    result = log_window(query,0,10000,7,True)
    assert result['total'] == 25 and result['limit'] == 20
    assert [r['id'] for r in result['items']] == [f'log-{i:02d}' for i in range(5,25)]
    assert all(r['message'] == text[-7:] and r['totalChars'] == len(text) and r['truncated'] for r in result['items'])
    assert db.query(TestSuiteLog.message).filter_by(id='log-24').scalar() == text
    log.info('25条大日志只取最近20条，中文emoji尾部/Unicode长度与截断标识正确，完整正文保持；不入队执行')


if __name__ == '__main__':
    try:
        spec = importlib.util.spec_from_file_location('mysql_fixture',ROOT/'scripts/verify_plan_native_http_mysql.py')
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        module.main(verify_request=verify)
    except Exception:
        log.exception('功能日志MySQL隔离验收失败'); raise
