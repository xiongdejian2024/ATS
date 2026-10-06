"""增量创建计划实例缺陷表，校验字段、主键、唯一约束与外键；默认仅预览。"""
import argparse
import sys
from pathlib import Path
from sqlalchemy import inspect, ForeignKeyConstraint, UniqueConstraint, Boolean
from sqlalchemy.dialects.mysql import TINYINT
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))
sys.path.insert(0, str(ROOT / 'scripts'))
from database import engine
import models
from models.plan_case_defect import PlanCaseDefect
from core.logger import logger
from upgrade_native_request_files import same_column_type


def upgrade(apply=False, connection_engine=None):
    target = connection_engine or engine
    table = PlanCaseDefect.__table__
    inspector = inspect(target)
    if table.name not in inspector.get_table_names():
        logger.info('计划实例缺陷表待创建：执行={}', apply)
        if apply: table.create(target, checkfirst=True)
        return [table.name]
    columns = {c['name']: c for c in inspector.get_columns(table.name)}
    if set(columns) != set(table.c.keys()) or any(columns[c.name]['nullable'] != c.nullable or not (isinstance(c.type, Boolean) and target.dialect.name == 'mysql' and isinstance(columns[c.name]['type'], TINYINT) and columns[c.name]['type'].display_width == 1 or same_column_type(columns[c.name]['type'], c.type, target.dialect)) for c in table.c):
        raise RuntimeError('已有实例缺陷表字段不兼容')
    if inspector.get_pk_constraint(table.name)['constrained_columns'] != [c.name for c in table.primary_key.columns]:
        raise RuntimeError('已有实例缺陷表主键不兼容')
    uniques = {tuple(c['column_names']) for c in inspector.get_unique_constraints(table.name)}
    for constraint in table.constraints:
        if isinstance(constraint, UniqueConstraint) and tuple(c.name for c in constraint.columns) not in uniques:
            raise RuntimeError('已有实例缺陷表缺少唯一约束')
        if isinstance(constraint, ForeignKeyConstraint):
            expected = (tuple(constraint.column_keys), next(iter(constraint.elements)).column.table.name,
                        tuple(fk.column.name for fk in constraint.elements), constraint.ondelete)
            actual = {(tuple(fk['constrained_columns']), fk['referred_table'], tuple(fk['referred_columns']), fk['options'].get('ondelete')) for fk in inspector.get_foreign_keys(table.name)}
            if expected not in actual: raise RuntimeError('已有实例缺陷表外键不兼容')
    indexes = {tuple(i['column_names']) for i in inspector.get_indexes(table.name)}
    if any(tuple(c.name for c in idx.columns) not in indexes for idx in table.indexes):
        raise RuntimeError('已有实例缺陷表索引不兼容')
    logger.info('计划实例缺陷表结构兼容，无需升级')
    return []


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    try: upgrade(parser.parse_args().apply)
    except Exception:
        logger.exception('计划实例缺陷表增量升级失败')
        raise
