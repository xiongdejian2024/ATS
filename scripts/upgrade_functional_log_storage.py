"""扩大MySQL功能执行日志容量；保留完整日志，幂等支持原TEXT与LONGTEXT。"""
import argparse
import sys
from pathlib import Path
from sqlalchemy import inspect, text
from sqlalchemy.dialects.mysql import TEXT, MEDIUMTEXT, LONGTEXT
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'backend'))
from database import engine
from core.logger import logger


def upgrade(apply=False, connection_engine=None):
    target = connection_engine or engine
    if target.dialect.name != 'mysql':
        logger.info('当前数据库无需日志容量升级：{}',target.dialect.name)
        return []
    columns = {c['name']:c for c in inspect(target).get_columns('test_suite_logs')}
    column = columns.get('message')
    if not column or column['nullable'] or not isinstance(column['type'], (TEXT, MEDIUMTEXT, LONGTEXT)):
        raise RuntimeError('已有日志正文列结构不兼容')
    if isinstance(column['type'], LONGTEXT):
        logger.info('完整日志容量已升级，无需重复修改')
        return []
    logger.info('功能执行日志待扩容LONGTEXT：执行={}',apply)
    if apply:
        with target.begin() as connection:
            original = column['type']
            type_sql = LONGTEXT(charset=original.charset,collation=original.collation).compile(dialect=target.dialect)
            connection.execute(text('ALTER TABLE test_suite_logs MODIFY COLUMN message '+type_sql+' NOT NULL COMMENT :comment'), {'comment':column.get('comment') or ''})
        logger.info('日志正文已扩容，原内容与其他列保持')
    return ['test_suite_logs.message']


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--apply',action='store_true')
    try:upgrade(parser.parse_args().apply)
    except Exception:logger.exception('功能日志容量升级失败');raise
